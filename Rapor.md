# Mikroservis Dağıtımı Ödevi Raporu

Bu rapor, mikroservis mimarisinin bulut benzeri bir ortama nasıl dağıtıldığını açıklanmaktadır. Ödev kapsamında istenen DevOps konseptleri, Altyapı otomasyonu ve Sürekli Dağıtım hedefleri başarıyla gerçekleştirilmiştir.

## 1. Ortam Konfigürasyonu (Environment Configuration)
Mikroservisler için gerekli ortam değişkenleri projeye hardcoded olarak verilmek yerine 12-factor uygulama prensiplerine uygun olarak `.env` dosyasına taşınmış ve `docker-compose.yml` üzerinde `env_file: .env` direktifiyle konfigürasyon yapılmıştır. Bu sayede servisler arasında daha güvenli ve dinamik bir yapı kurulmuştur.

## 2. Otomatik Testler (Automated Tests)
Servislerin sağlıklı çalıştığından emin olmak için `pytest`, `pytest-asyncio` ve `httpx` kütüphaneleri `requirements.txt` dosyasına eklenmiştir.
- **Auth Service:** Kullanıcı kayıt (register) ve giriş (login) operasyonlarını doğrulayan testler yazıldı.
- **Note Service:** Gateway üzerinden not oluşturma operasyonu RabbitMQ ve Auth Service bağımlılıkları mocklanarak test edildi.
- **API Gateway:** İsteklerin başarıyla ilgili servislere yönlendirildiği test edildi.

## 3. CI/CD Pipeline
Sürekli entegrasyon için **GitHub Actions** tercih edildi. Proje kök dizininde oluşturulan `.github/workflows/ci.yml` konfigürasyonuyla; `main` branch'ine yapılan her 'push' veya 'pull request' tetiklendiğinde:
- Python bağımlılıkları yüklenmektedir.
- Tüm `pytest` test suite'leri çalıştırılmaktadır.
- Projenin `docker-compose build` komutu kullanılarak Docker image'ları derlenip build sürecinin sorunsuz geçtiği kontrol edilmektedir.

## 4. Container Orchestration (Kubernetes Dağıtımı)
Mikroservislerin ölçeklenebilir bir yapıya kavuşması adına `Docker Compose`'un ötesine geçilerek Kubernetes ortamında çalışmalarını sağlayacak `k8s/` manifestoları hazırlandı.
- Her mikroservis için `Deployment` ve `Service` yaml dosyaları oluşturuldu (`auth-service.yaml`, `api-gateway.yaml`, `note-service.yaml`, vb).
- `.env` yönetiminin Kubernetes karşılığı olarak `config.yaml` altında bir **ConfigMap** ve **Secret** tanımlandı. Tüm podlar çevre değişkenlerini buradan alacak şekilde revize edildi.

## 5. Deployment Script
Tüm sistemi tek bir tıkla yerel bir Kubernetes kümesinde (Minikube veya Docker Desktop Kubernetes) ayağa kaldırmak için `deploy.ps1` PowerShell scripti oluşturuldu. Bu script öncelikle konfigürasyonları ve message broker'ı (RabbitMQ) ayağa kaldırıp ardından servis dağıtımlarını gerçekleştirmektedir.

Tüm "Deliverables" (CI/CD dosyası, deployment script'i ve testler) sağlanmış ve sistemin canlıya çıkabilir durumu demonstre edilmiştir.
