# Pake Alphine biar image lebih kecil, tapi harus install build-base dulu kalo mau compile package tertentu
# At least enteng ya, biar dosa aja yang berat, script jangan
FROM python:3.11-alpine

# Label metadata (opsional sih, tapi bagus buat pamer, ganteng, dan biar orang tau siapa yang bikin)
LABEL maintainer="amiencoy"
LABEL description="Reconnator - Modern Cloud-Native Recon Bot"

WORKDIR /app

# Copy file requirements duluan biar layer cache Docker bisa dipake kalo requirements.txt ga berubah
COPY requirements.txt .

# Install dependencies doang tapi ga sisain cache, biar layer cache bisa dipake kalo requirements.txt ga berubah
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh folder source code (src), terus di compile jadi image Docker
COPY src/ ./src/

# Command default doang sih, tapi bisa di override kalo mau pake docker run -it --rm <image> <command>, terserah anda aja maunya gimana, kan udah gede
ENTRYPOINT ["python", "src/main.py"]
# Udah sih, gitu aja
#
#
#
#
#
#
#
#....
#
#.......
#
#
#
#
#
#
#
# Tapi boong XD
#
#
#
#
#.....
#
#
# Ga deng ga boong, beneran sih, gitu aja <<<*vv*>>>