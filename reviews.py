from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException


def main(param_dict):
    db_name = "reviews"
    try:
        authenticator = IAMAuthenticator(param_dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(param_dict["COUCH_URL"])

        if "dealerId" in param_dict:
            selected = service.post_find(db=db_name, selector={"dealership": int(param_dict["dealerId"])})
            return { "body": selected.result['docs']}
        else:
            reviews = service.post_all_docs(db=db_name, include_docs=True)
            return {"body": [i['doc'] for i in reviews.result['rows']]}

    except ApiException as ae:
        if ("reason" in ae.http_response.json()):
            return {"error": ae.http_response.json()["reason"]}
        return {"status_code": ae.code, "error_message": ae.message}


