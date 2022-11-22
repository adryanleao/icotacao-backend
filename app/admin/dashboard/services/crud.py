from sqlalchemy import func

from app.admin.company.models import Company
from app.admin.user.models import User
from app.client.quote.models import Quote, QuoteProposal


def get_dashboard():
    companies_active = Company.query.filter(
        Company.deleted_at.is_(None)).count()
    companies_inactive = Company.query.filter(
        Company.deleted_at.isnot(None)).count()

    quotes_total = Quote.query.filter(Quote.deleted_at.is_(None)).count()
    quotes_approved = Quote.query.filter(Quote.deleted_at.is_(None),
                                         Quote.status == 2).count()
    quotes_amount = QuoteProposal.query.with_entities(
        func.sum(QuoteProposal.price + QuoteProposal.delivery_price).label(
            "total_price")).filter(QuoteProposal.deleted_at.is_(None),
                                   Quote.status == 2).scalar()

    dict_return = {
        "companies": {
            "active": companies_active,
            "inactive": companies_inactive
        },
        "quotes": {
            "total": quotes_total,
            "approved": quotes_approved,
            "amount": quotes_amount
        }
    }

    return dict_return
