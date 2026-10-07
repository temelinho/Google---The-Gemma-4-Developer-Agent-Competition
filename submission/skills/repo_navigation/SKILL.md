---
name: repo_navigation
description: Buyuk bir repoda ilgili kodu hizli bulma teknikleri.
---

# Repo gezinme becerisi

Buyuk kod tabanlarinda hatayi bulmak, duzeltmekten daha zor. Sirayla:

1. Issue metnindeki anahtar kelimelerle `search_similar_code` calistir.
2. En benzer dugumleri `get_code_neighbors` ile genislet.
3. Birkac supheli sembolu `get_code_subgraph` ile birlikte incele.
4. Ancak daralttiktan sonra `read_file` ile gercek kodu oku.

Amac: tum dosyalari okumadan, grafik uzerinden hedefe gitmek.
