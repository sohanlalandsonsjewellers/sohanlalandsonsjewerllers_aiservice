from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationModel:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

    def recommend(
        self,
        products,
        product_id,
        top_k=5
    ):

        if len(products) == 0:

            return []

        corpus = []

        for product in products:

            corpus.append(

                f"{product['name']} "
                f"{product['category']} "
                f"{product['subCategory']} "
                f"{product['description']}"

            )

        tfidf = self.vectorizer.fit_transform(
            corpus
        )

        similarity = cosine_similarity(
            tfidf,
            tfidf
        )

        index = None

        for i, product in enumerate(products):

            if product["id"] == product_id:

                index = i

                break

        if index is None:

            return []

        scores = list(
            enumerate(
                similarity[index]
            )
        )

        scores = sorted(

            scores,

            key=lambda x: x[1],

            reverse=True

        )

        recommendations = []

        for i, score in scores[1: top_k + 1]:

            recommendations.append({

                "id": products[i]["id"],

                "name": products[i]["name"],

                "category": products[i]["category"],

                "price": products[i]["price"],

                "score": round(
                    float(score),
                    4
                )

            })
            

        return recommendations

        