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

        if len(customers) < 4:

            return []

        X = []

        for customer in customers:

            X.append([

                customer["totalOrders"],

                customer["totalSpent"]

            ])

        X = np.array(X)

        labels = self.model.fit_predict(X)

        centers = self.model.cluster_centers_

        cluster_info = {}

        for i, center in enumerate(centers):

            cluster_info[i] = {

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

        segment_map = {}

        names = [

            "VIP",

            "Premium",

            "Regular",

            "New Customer"

        ]

        for index, (cluster_id, _) in enumerate(sorted_clusters):

            segment_map[cluster_id] = names[index]

        result = []

        for index, customer in enumerate(customers):

            result.append({

                **customer,

                "segment": segment_map[labels[index]]

            })
        
        
        result = []

        for index, customer in enumerate(customers):

            result.append({

        **customer,

        "cluster": int(labels[index]),

        "segment": segment_map[int(labels[index])]

    })


        segment_priority = {

            "VIP": 0,

            "Premium": 1,

            "Regular": 2,

            "New Customer": 3

        }

        result.sort(

            key=lambda x: (

                segment_priority[x["segment"]],

                -x["totalSpent"],

                -x["totalOrders"]

            )

        )

        return result