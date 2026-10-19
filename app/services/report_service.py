import io
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ACCENT = colors.HexColor("#1c5a92")
MUTED = colors.HexColor("#666677")
RULE = colors.HexColor("#d9d9e6")
SHADE = colors.HexColor("#f0eefc")

_base = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "Title", parent=_base["Title"], alignment=0, fontSize=22, spaceAfter=2
)
SUBTITLE = ParagraphStyle(
    "Subtitle", parent=_base["Normal"], textColor=MUTED, fontSize=9, spaceAfter=10
)
HEADING = ParagraphStyle(
    "Heading",
    parent=_base["Heading2"],
    textColor=ACCENT,
    fontSize=12,
    spaceBefore=14,
    spaceAfter=4,
)
BODY = ParagraphStyle("Body", parent=_base["Normal"], fontSize=10, leading=14)
LABEL = ParagraphStyle("Label", parent=BODY, textColor=MUTED, fontSize=8)


def _p(text, style=BODY):
    """Paragraph with user text escaped, because Paragraph parses its input as markup."""
    return Paragraph(escape(str(text)), style)


def _money(value):
    return f"${float(value):,.2f}"


def _table(rows, col_widths, header=None, right_align_from=None, total_row=False):
    """A simple ruled table. `rows` are lists of cell strings."""
    data = ([header] if header else []) + rows
    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), SHADE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    if right_align_from is not None:
        style.append(("ALIGN", (right_align_from, 0), (-1, -1), "RIGHT"))
    if total_row:
        style.append(("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"))
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle(style))
    return table


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 10 * mm, "ReefWatch Marine Conservation")
    canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def survey_pdf(survey):
    """Render one survey document as a PDF and return the bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title=f"Survey {survey['_id']}",
        author="ReefWatch",
    )
    width = A4[0] - doc.leftMargin - doc.rightMargin
    researcher = survey.get("researcher", {})
    species = survey.get("species", [])
    equipment = survey.get("equipmentUsed", [])

    story = [
        _p(f"Survey report: {survey['surveyDate']}", TITLE),
        _p(f"{survey['_id']} · Station {survey.get('stationId', '—')}", SUBTITLE),
        _table(
            [
                ["Site", survey["site"]],
                ["Researcher", researcher.get("name", "—")],
                ["Email", researcher.get("email") or "—"],
                ["Total cost", _money(survey["totalCost"])],
            ],
            [35 * mm, width - 35 * mm],
        ),
        _p("Species observed", HEADING),
    ]

    species_rows = [[s["name"], str(s["count"])] for s in species]
    species_rows.append(["Total individuals", str(sum(s["count"] for s in species))])
    story.append(
        _table(
            species_rows,
            [width - 30 * mm, 30 * mm],
            header=["Species", "Count"],
            right_align_from=1,
            total_row=True,
        )
    )

    story.append(_p("Equipment used", HEADING))
    if equipment:
        story.append(
            _table(
                [[e["name"], e["equipmentId"], str(e["quantity"])] for e in equipment],
                [width - 60 * mm, 30 * mm, 30 * mm],
                header=["Item", "ID", "Qty"],
                right_align_from=2,
            )
        )
    else:
        story.append(_p("No equipment recorded.", LABEL))

    if survey.get("createdAt"):
        story += [
            Spacer(1, 10 * mm),
            _p(
                "Recorded " + survey["createdAt"][:16].replace("T", " ") + " UTC", LABEL
            ),
        ]

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
