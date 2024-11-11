import requests
import os
from datetime import datetime
import svgwrite

# GitHub kullanıcısının commit bilgilerini alır.
def get_commit_data():
    token = os.getenv("GITHUB_TOKEN")
    owner, repo = os.getenv("GITHUB_REPOSITORY").split('/')
    headers = {"Authorization": f"Bearer {token}"}

    # Geçmiş 30 günün commit sayısını çekiyoruz.
    since = (datetime.utcnow() - timedelta(days=30)).isoformat() + "Z"
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={since}"

    response = requests.get(url, headers=headers)
    return len(response.json())

# Bitkisel büyüme SVG'si oluşturma.
def generate_plant_growth(commit_count):
    dwg = svgwrite.Drawing('dist/plant_growth.svg', profile='tiny', size=(200, 200))
    
    # Zemine toprak çizimi
    dwg.add(dwg.rect(insert=(0, 150), size=(200, 50), fill='brown'))

    # Her commit bir filiz olarak eklenecek
    base_y = 150
    base_x = 100
    height_increment = 5

    for i in range(commit_count):
        stem_height = height_increment * (i + 1)
        dwg.add(dwg.line(start=(base_x, base_y), end=(base_x, base_y - stem_height), stroke="green", stroke_width=2))
        base_y -= height_increment

    # Üstte bir yaprak ekleyelim
    dwg.add(dwg.circle(center=(base_x, base_y - 5), r=5, fill="green"))

    # Dosyayı kaydet
    dwg.save()

if __name__ == "__main__":
    commit_count = get_commit_data()
    generate_plant_growth(commit_count)
