from app.admin.user.services.crud import get_user
from app.auth.services.user import get_user_jwt
from app.client.quote.models import QuoteProposal


def verify_proposal(quote):
    user_jwt = get_user_jwt()
    user = get_user(user_jwt["user_id"])
    proposal = QuoteProposal.query.filter(QuoteProposal.quote_id == quote["id"],
                                           QuoteProposal.company_id == user.company_id,
                                           QuoteProposal.deleted_at == None).first()
    proposal_sent = proposal.id if proposal else None
    return proposal_sent
