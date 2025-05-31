# 🤖 Chatbot WhatsApp - Luar Clínica 

*Sistema automatizado para agendamentos e informações via WhatsApp Cloud API da Meta, com compliance LGPD e segurança de dados.*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![Meta API](https://img.shields.io/badge/Meta%20WhatsApp%20API-Cloud-green)
![LGPD](https://img.shields.io/badge/Compliance-LGPD-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

## 🌟 Funcionalidades
- **Agendamento automático** para procedimentos:
  - 👂 Perfuração de piercing (22 etapas)
  - ✨ Remoção de queloide
  - 🎨 Remoção de tatuagem
  - ⚕️ Tratamento de granuloma
- **Informações instantâneas**:
  - 💰 Tabela de preços
  - 🩹 Cuidados pós-procedimento
- **Proteção de dados**:
  - 🔒 Consentimento explícito (LGPD)
  - 🗑️ Exclusão sob demanda (`EXCLUIR DADOS`)
  - 🕵️ Mascaramento de dados sensíveis
- **Gestão de sessões**:
  - ⏳ Timeout após 5 minutos
  - 🧹 Auto-destruição em 24h

## 🛠️ Estrutura do Código
```plaintext
Chatbot/
├── Core/
│   ├── tempo_sessao.py       # Gerencia tempo de sessão (5m/24h)
│   └── whatsapp_api.py       # Comunicação com API Meta
│
├── Fluxos/
│   ├── fluxo_base.py         # Classe base abstrata
│   ├── fluxo_piercing.py     # Fluxo completo (nome, idade, 20 perguntas de saúde)
│   ├── fluxo_queloide.py     # Remoção de queloide
│   ├── fluxo_remocao_tattoo.py # Remoção de tatuagem
│   ├── fluxo_granuloma.py    # Tratamento de granuloma
│   ├── fluxo_piercing_preco.py # Tabela de preços
│   └── fluxo_piercing_cuidados.py # Cuidados pós-procedimento
│
└── app.py                    # Servidor Flask (webhook)


⚙️ Configuração
Pré-requisitos

    Conta de desenvolvedor Meta (Cadastro)

    Número empresarial no WhatsApp

    Domínio com HTTPS (luarclinica.com.br)

    Python 3.9+

Passo a Passo

    Clone o repositório:
    git clone https://github.com/seu-usuario/luar-chatbot.git
    cd luar-chatbot

    Instale as dependências:
    pip install flask python-dotenv requests

    Crie o arquivo .env:
    # Tokens da Meta
    WHATSAPP_TOKEN="seu_token_da_api"
    VERIFY_TOKEN="seu_token_de_verificacao"
    PHONE_NUMBER_ID="ID_do_seu_numero"

    # Configurações opcionais
    SESSION_TIMEOUT=300  # 5 minutos em segundos

🚀 Como Executar

Modo desenvolvimento:
python app.py


🔍 Fluxo de Mensagens

Início
→ Usuário envia 1
← Bot solicita consentimento

Consentimento
→ Usuário responde ACEITO
← Bot mostra menu:



🔒 Compliance LGPD

Dados coletados:

Nome completo (armazenado mascarado)

Idade

Informações de saúde (apenas com CONCORDO)

Proteções:
    # Exemplo de sanitização (whatsapp_api.py)
    def sanitize_message(self, message):
        sensitive_terms = ["CPF", "RG", "cartão"]
        for term in sensitive_terms:
            message = message.replace(term, "[DADO PROTEGIDO]")
        return message


📬 Suporte Técnico

Equipe Luar Clínica
✉️ admin@luarclinica.com.br
📞 +55 69 9397-9351

Desenvolvedor
✉️ admin@luarclinica.com.br

Política de Privacidade | Termos de Uso : https://luarclinica.com.br/

