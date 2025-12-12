import random


ADMINS = [539442908]
API_ID = 22648887
API_HASH ="14b84546a0f135c74e849260019da905"

devices = ['Samsung Galaxy A10', 'Samsung Galaxy A10s', 'Samsung Galaxy A30', 'Samsung Galaxy A40', 'Samsung Galaxy A70', 'Samsung Galaxy A71', 'LG LBELLO', 'Oppo A73', 'Poco C3', 'Oppo A93', 'Samsung Galaxy A3 Core', 'Xiaomi Mi 10T Lite 5G', 'Vivo X50E 5G', 'Infinix Hot 10 Lite', 'Samsung Galaxy A80', 'Huawei P Smart 2021', 'Gionee S12 Lite', 'Oppo A33', 'Xiaomi Mi 10T Pro 5G', 'Xiaomi Mi 10T 5G', 'LG K10', 'LG K52', 'LG K62', 'LG K71', 'Nokia 3.4', 'Poco X3', 'Honor 20 Lite', 'Honor 8S 2020', 'Honor 10 Lite', 'Honor 8A', 'Honor 9X Lite', 'Sony Xperia 5', 'Sony Xperia L4', 'Sony Xperia 10', 'Samsung S20', 'Samsung Galaxy Note 20 Ultra 5G', 'Samsung S10+', 'Samsung Galaxy S20 5G', 'Samsung Galaxy S20+ 5G', 'Samsung Galaxy A21s', 'Samsung Galaxy A51', 'Samsung Galaxy S10 Lite', 'Samsung Galaxy S9', 'Samsung Galaxy S8', 'Samsung Galaxy A41']
versions = ["T10.0.1 - P11.1.1"]
appvs = ["1.35.1 (1359)"]


def get_random_device():
    devices = [
        {"MANUFACTURER": "Gionee", "MODEL": "S12 Lite", "SDK": 29},
        {"MANUFACTURER": "Honor", "MODEL": "10 Lite", "SDK": 29},
        {"MANUFACTURER": "Honor", "MODEL": "20 Lite", "SDK": 29},
        {"MANUFACTURER": "Honor", "MODEL": "8A", "SDK": 28},
        {"MANUFACTURER": "Honor", "MODEL": "9X Lite", "SDK": 29},
        {"MANUFACTURER": "Huawei", "MODEL": "P Smart 2021", "SDK": 29},
        {"MANUFACTURER": "Infinix", "MODEL": "Hot 10 Lite", "SDK": 29},
        {"MANUFACTURER": "LG", "MODEL": "K52", "SDK": 29},
        {"MANUFACTURER": "LG", "MODEL": "K62", "SDK": 29},
        {"MANUFACTURER": "LG", "MODEL": "K71", "SDK": 29},
        {"MANUFACTURER": "Nokia", "MODEL": "3.4", "SDK": 30},
        {"MANUFACTURER": "Oppo", "MODEL": "A33", "SDK": 29},
        {"MANUFACTURER": "Oppo", "MODEL": "A73", "SDK": 29},
        {"MANUFACTURER": "Oppo", "MODEL": "A93", "SDK": 29},
        {"MANUFACTURER": "Poco", "MODEL": "C3", "SDK": 29},
        {"MANUFACTURER": "Poco", "MODEL": "X3", "SDK": 30},
        {"MANUFACTURER": "Sony", "MODEL": "Xperia 10", "SDK": 29},
        {"MANUFACTURER": "Sony", "MODEL": "Xperia 5", "SDK": 29},
        {"MANUFACTURER": "Vivo", "MODEL": "X50E 5G", "SDK": 29},
        {"MANUFACTURER": "Xiaomi", "MODEL": "Mi 10T 5G", "SDK": 31},
        {"MANUFACTURER": "Xiaomi", "MODEL": "Mi 10T Lite 5G", "SDK": 31},
        {"MANUFACTURER": "Xiaomi", "MODEL": "Mi 10T Pro 5G", "SDK": 31},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy A10", "SDK": 30},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy A21s", "SDK": 31},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy A51", "SDK": 31},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy A71", "SDK": 31},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy Note 20 Ultra 5G", "SDK": 33},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy S10 Lite", "SDK": 31},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy S20 5G", "SDK": 33},
        {"MANUFACTURER": "Samsung", "MODEL": "Galaxy S8", "SDK": 28},
    ]
    return random.choice(devices)
