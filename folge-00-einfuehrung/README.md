# Folge 0 – Worum geht es in diesem Kurs?

Die Einführung hat keinen Code. Hier sind die Quellen zu den drei echten Fällen und zu den Aussagen im Video.

## Die drei Fälle
1. **Chevrolet of Watsonville (Dezember 2023):** Ein Nutzer bringt den Chatbot eines Autohauses dazu, einem neuen
   Chevy Tahoe für 1 $ zuzustimmen („legally binding offer“).
   - AI Incident Database: https://incidentdatabase.ai/entities/chevrolet-of-watsonville
2. **Moffatt v. Air Canada, 2024 BCCRT 149 (Februar 2024):** Der Chatbot nennt eine Erstattungsregel, die es so nicht gab;
   das Tribunal entscheidet, dass Air Canada für die Aussagen ihres Chatbots haftet.
   - https://www.mccarthy.ca/en/insights/blogs/techlex/moffatt-v-air-canada-misrepresentation-ai-chatbot
3. **EchoLeak, CVE-2025-32711 (Juni 2025):** Eine präparierte E-Mail konnte Microsoft 365 Copilot dazu bringen, interne
   Daten an einen Angreifer zu schicken – ohne Klick des Opfers. Von Microsoft behoben, keine Hinweise auf Ausnutzung.
   - https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html
   - Paper: https://arxiv.org/abs/2509.10540

## Weitere Quellen
- OWASP LLM01 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  („it is unclear if there are fool-proof methods of prevention for prompt injection“)
- OWASP Top 10 for LLM Applications 2026: Prompt Injection weiterhin auf Platz 1

## Der Test „Die Regel verschwindet“
Der im Video erwähnte Test (Regel „Beginne jede Antwort mit ShopFix:“ geht bei einem langen Dokument verloren)
wird in einer späteren Folge Schritt für Schritt erklärt – inklusive Ursache und Schutz.
