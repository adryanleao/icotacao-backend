from app.admin.company.models import CompanySegment


def create_segment_company(company_id, segments):
    segments_return = []
    for segment_id in segments:
        dict_body = {
            "company_id": company_id,
            "segment_id": segment_id
        }
        segments_return.append(CompanySegment().create_item(dict_body).save())

    return segments_return


def update_segment_company(company_id, segments):
    segments = [segment["id"] for segment in segments if segment.get("id")]
    segments_delete = CompanySegment.query.filter(CompanySegment.id.notin_(segments)).all()
    for segment_delete in segments_delete:
        segment_delete.delete_real()

    segments_return = []
    for segment in segments:
        segment_dict = {
            "segment_id": segment,
            "company_id": company_id
        }
        segments_return.append(CompanySegment().create_item(segment_dict).save())

    return segments_return
