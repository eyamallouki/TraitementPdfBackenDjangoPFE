from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import spacy
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import logging
from collections import Counter
from heapq import nlargest
from .models import PDF

logger = logging.getLogger(__name__)

# Assurez-vous que le modèle spaCy est téléchargé et chargé
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    from spacy.cli import download
    download("fr_core_news_sm")
    nlp = spacy.load("fr_core_news_sm")


class DocumentProcessingView(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        command = request.data.get("command", "").lower()
        rapport_id = request.data.get("rapport_id", None)
        if not command or not rapport_id:
            return JsonResponse({"error": "Command or rapport_id not provided"}, status=400)

        if "résumé" in command:
            return self.resumer_rapport(rapport_id)
        elif "ocr" in command:
            return self.ocr_rapport(rapport_id)
        else:
            return JsonResponse({"message": "Command not recognized"}, status=400)

    def resumer_rapport(self, rapport_id):
        try:
            rapport = PDF.objects.get(id=rapport_id)

            if rapport.filtered_text:
                text_to_summarize = rapport.filtered_text
            else:
                text_to_summarize = self.extract_text_from_pdf(rapport.file.path)
                rapport.filtered_text = text_to_summarize
                rapport.save()

            cleaned_text = self.clean_text(text_to_summarize)
            summary = self.generate_summary(cleaned_text)

            return JsonResponse({"summary": summary}, status=200)

        except PDF.DoesNotExist:
            return JsonResponse({"error": "Rapport not found"}, status=404)
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()

            if not page_text.strip():  # Si le texte est vide, appliquer l'OCR
                logger.info(f"Applying OCR on page {page_num + 1} because no text was found.")
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                page_text = pytesseract.image_to_string(img, lang='fra')

            text += page_text + "\n"

        return text

    def clean_text(self, text):
        doc = nlp(text)
        content_sentences = []

        for sent in doc.sents:
            if len(sent.text.split()) > 2 and any(token.pos_ == "VERB" for token in sent):
                content_sentences.append(sent.text)

        return " ".join(content_sentences)

    def generate_summary(self, text, summary_length=10):  # Augmenter le nombre de phrases dans le résumé
        doc = nlp(text)
        sentence_tokens = [sent for sent in doc.sents]

        word_frequencies = Counter([token.text.lower() for token in doc if not token.is_stop and not token.is_punct])

        sentence_scores = {
            sent: sum(word_frequencies[token.text.lower()] for token in sent if token.text.lower() in word_frequencies)
            for sent in sentence_tokens
        }

        # Sélectionner les phrases avec un seuil minimal de fréquence
        summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
        summary = " ".join([sent.text for sent in summary_sentences])

        # Filtrer les phrases pour éliminer les résumés incohérents ou hors sujet
        filtered_summary = self.filter_summary(summary)

        return filtered_summary

    def filter_summary(self, summary):
        """Filtrer le résumé pour supprimer les phrases incohérentes ou hors sujet."""
        doc = nlp(summary)
        filtered_sentences = []

        for sent in doc.sents:
            if any(token.pos_ == "NOUN" for token in sent) and any(token.pos_ == "VERB" for token in sent):
                filtered_sentences.append(sent.text)

        return " ".join(filtered_sentences)
