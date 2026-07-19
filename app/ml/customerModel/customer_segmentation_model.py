import numpy as np
from sklearn.cluster import KMeans


class CustomerSegmentationModel:

    def __init__(self):

        self.model = KMeans(
            n_clusters=4,
            random_state=42,
            n_init="auto"
        )

    def segment(self, customers):

        if not customers:
            return []

        # Small Dataset
        if len(customers) < 4:

            for customer in customers:

                spent = customer["totalSpent"]
                orders = customer["totalOrders"]

                if orders <= 1:

                    customer["cluster"] = 3
                    customer["segment"] = "New Customer"

                elif orders >= 5 or spent >= 20000:

                    customer["cluster"] = 0
                    customer["segment"] = "VIP"

                elif orders >= 2 or spent >= 5000:

                    customer["cluster"] = 1
                    customer["segment"] = "Premium"

                else:

                    customer["cluster"] = 2
                    customer["segment"] = "Regular"

            return customers

        # ----------------------------
        # ML Clustering
        # ----------------------------

        X = np.array(

            [

                [
                    customer["totalOrders"],
                    customer["totalSpent"]
                ]

                for customer in customers

            ]

        )

        labels = self.model.fit_predict(X)

        centers = self.model.cluster_centers_

        cluster_info = {}

        for index, center in enumerate(centers):

            cluster_info[index] = {

                "orders": center[0],
                "spent": center[1]

            }

        sorted_clusters = sorted(

            cluster_info.items(),

            key=lambda x: (

                x[1]["spent"],
                x[1]["orders"]

            ),

            reverse=True

        )

        names = [

            "VIP",
            "Premium",
            "Regular",
            "New Customer"

        ]

        segment_map = {}

        for index, (cluster_id, _) in enumerate(sorted_clusters):

            segment_map[int(cluster_id)] = names[index]

        result = []

        for index, customer in enumerate(customers):

            segmented_customer = {

                **customer,

                "cluster": int(labels[index]),

                "segment": segment_map[int(labels[index])]

            }

            # ----------------------------
            # Business Rule Overrides
            # ----------------------------

            orders = segmented_customer["totalOrders"]
            spent = segmented_customer["totalSpent"]

            if orders <= 1:

                segmented_customer["segment"] = "New Customer"

            elif orders >= 5 or spent >= 20000:

                segmented_customer["segment"] = "VIP"

            elif orders >= 2 or spent >= 5000:

                segmented_customer["segment"] = "Premium"

            else:

                segmented_customer["segment"] = "Regular"

            result.append(segmented_customer)

        priority = {

            "VIP": 0,
            "Premium": 1,
            "Regular": 2,
            "New Customer": 3

        }

        result.sort(

            key=lambda customer: (

                priority.get(
                    customer["segment"],
                    99
                ),

                -customer["totalSpent"],

                -customer["totalOrders"]

            )

        )

        return result