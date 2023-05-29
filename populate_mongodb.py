"""
Store ICPSR subject thesaurus in MongoDB.
"""

import os

import pandas as pd

from util import TermRelationshipID, TermRelationshipName, get_mongo_collection


DATA_DIR = "/ssd/congtj/icpsr_data/subject_thesaurus"
SUBJECT_TERM_FILEPATH = os.path.join(DATA_DIR, "subject_terms.xlsx")
TERM_REL_FILEPATH = os.path.join(DATA_DIR, "term_relations.xlsx")


if __name__ == "__main__":
    subject_terms = pd.read_excel(SUBJECT_TERM_FILEPATH, usecols=["TERM_ID", "TERM"])
    term_rels = pd.read_excel(TERM_REL_FILEPATH, usecols=["SUBJECT_ID", "RELATIONSHIP", "OBJECT_ID", "OBJECT_TERM"])

    merged_df = subject_terms.merge(term_rels, how="left", left_on="TERM_ID", 
                                    right_on="SUBJECT_ID", 
                                    validate="one_to_many")
    
    mongo_client, mongo_col = get_mongo_collection()
    
    for group_id, group in merged_df.groupby("TERM_ID"):
        document = {"term_id": group_id}
        document["term"] = group.iloc[0]["TERM"]
        document["term_in_lowercase"] = group.iloc[0]["TERM"].lower()

        for _, row in group.iterrows():
            assert row["TERM_ID"] == group_id

            if row["RELATIONSHIP"] == TermRelationshipID.NARROWER.value:
                if TermRelationshipName.NARROWER.value in document:
                    document[TermRelationshipName.NARROWER.value].append(
                        row["OBJECT_TERM"])
                else:
                    document[TermRelationshipName.NARROWER.value] = [
                        row["OBJECT_TERM"]]
            elif row["RELATIONSHIP"] == TermRelationshipID.BROADER.value:
                if TermRelationshipName.BROADER.value in document:
                    document[TermRelationshipName.BROADER.value].append(
                        row["OBJECT_TERM"])
                else:
                    document[TermRelationshipName.BROADER.value] = [
                        row["OBJECT_TERM"]]
            elif row["RELATIONSHIP"] == TermRelationshipID.RELATED.value:
                if TermRelationshipName.RELATED.value in document:
                    document[TermRelationshipName.RELATED.value].append(
                        row["OBJECT_TERM"])
                else:
                    document[TermRelationshipName.RELATED.value] = [
                        row["OBJECT_TERM"]]
            elif row["RELATIONSHIP"] == TermRelationshipID.PREFERRED.value:
                if TermRelationshipName.PREFERRED.value in document:
                    document[TermRelationshipName.PREFERRED.value].append(
                        row["OBJECT_TERM"])
                else:
                    document[TermRelationshipName.PREFERRED.value] = [
                        row["OBJECT_TERM"]]
            elif row["RELATIONSHIP"] == TermRelationshipID.NONPREFERRED.value:
                if TermRelationshipName.NONPREFERRED.value in document:
                    document[TermRelationshipName.NONPREFERRED.value].append(
                        row["OBJECT_TERM"])
                else:
                    document[TermRelationshipName.NONPREFERRED.value] = [
                        row["OBJECT_TERM"]]
            else:
                continue

        mongo_col.insert_one(document)
    
    mongo_client.close()
