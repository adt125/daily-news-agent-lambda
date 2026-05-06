import logging

logger = logging.getLogger(__name__)


def generate_html_email(data):
    ai_count = len(data.get("ai", []))
    market_count = len(data.get("market", []))
    logger.info("Generating HTML email. AI items=%s Market items=%s", ai_count, market_count)

    def render_section(title, items):
        section_html = f"<h2 style='margin-top:20px;'>{title}</h2>"

        for item in items:
            section_html += f"""
            <div style="margin-bottom:20px;">
                <p style="font-weight:bold; margin:0;">
                    {item.get("title", "")}
                </p>
                <p style="margin:5px 0;">
                    {item.get("summary", "")}
                </p>
                <a href="{item.get("link", "#")}" 
                   style="color:#1a73e8; text-decoration:none;">
                   Read full news →
                </a>
            </div>
            """

        return section_html

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height:1.6; max-width:600px; margin:auto;">
        <p>Hello AI & Market Enthusiast,</p>

        {render_section("AI Updates", data.get("ai", []))}
        {render_section("Market Updates", data.get("market", []))}

        <p style="margin-top:30px;">
            Stay informed,<br>
            <strong>MarketMind AI</strong>
        </p>
    </body>
    </html>
    """

    logger.info("HTML email generated")
    return html
