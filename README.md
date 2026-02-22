โปรเจกต์นี้ดึงข้อมูลราคาหุ้นและข่าวสารมาวิเคราะห์หาความสัมพันธ์ระหว่าง Sentiment และการเคลื่อนที่ของราคาหุ้น โดยทำงานแบบอัตโนมัติบน Cloud

## **Tech stack**
-   **Language:** Python (Pandas, Matplotlib)
    
-   **Data Source:** Yahoo Finance API (`yfinance`)
    
-   **Sentiment Analysis:** VADER Sentiment Analysis
    
-   **Database:** PostgreSQL (Docker) สำหรับ Local Development
    
-   **Automation:** GitHub Actions (CI/CD) สำหรับการรันงานบน Cloud
    
-   **OS:** Ubuntu (GitHub Runner)

## Pipeline Architecture
ระบบถูกออกแบบมาให้ทำงาน 4 ขั้นตอนหลัก ดังนี้:

1.  **Data Ingestion (การดึงข้อมูล):** ใช้ข้อมูล `yfinance` เพื่อดึงราคาหุ้นรายชั่วโมง และพาดหัวข่าวล่าสุดของหุ้นกลุ่มธนาคาร (BBL, SCB, KTB)
    
2.  **Sentiment Processing (การวิเคราะห์ความรู้สึก):** นำพาดหัวข่าวมาผ่านโมเดล **VADER (Valence Aware Dictionary and sEntiment Reasoner)** เพื่อแปลงข้อความเป็นตัวเลข **Sentiment Score** ในช่วง $-1$ (ข่าวไม่ดี) ถึง $1$ (ข่าวดี)
        
3.  **Hybrid Data Storage (การจัดเก็บข้อมูล):**
    
    -   **Local:** จัดเก็บลง **PostgreSQL Database** ที่รันบน **Docker**
        
    -   **Cloud:** เมื่อรันผ่าน **GitHub Actions** ระบบจะบันทึกเป็นไฟล์ **CSV**
        
4.  **Data Visualization (การสรุปผล):**
    
    -   ประมวลผลข้อมูลรายชั่วโมงและสร้างกราฟ เพื่อเปรียบเทียบความสัมพันธ์ระหว่างราคา (เส้นสีน้ำเงิน) และความรู้สึกของข่าว (แท่งสีส้ม)
