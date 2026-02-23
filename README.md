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


<img width="1400" height="700" alt="SCB BK" src="https://github.com/user-attachments/assets/fde17acc-560e-40a5-acf4-b4b379dbe2bd" />

ธนาคารไทยพาณิชย์ (SCB.BK): สำหรับ SCB พบว่าราคาค่อย ๆไปในทิศทางบวกจาก 142 บาท ขึ้นไป 148 บาท คะแนน Sentiment ยังอยู่ในทางที่ดีอยู่ ในช่วงเช้าวันที่ 23 ก.พ. ส่งผลให้ราคาสามารถทรงตัวได้




<img width="1400" height="700" alt="BBL BK" src="https://github.com/user-attachments/assets/6f1e37e0-9b7b-40d0-ad29-f9ff6eee5a94" />

ธนาคารกรุงเทพ (BBL.BK): หุ้น BBL แสดงสภาวะขาขึ้น โดยราคาพุ่งจากระดับ 162 บาท ไปถึง 176 บาท ซึ่งสอดคล้องอย่างมีนัยสำคัญกับคะแนน Sentiment เชิงบวกที่พุ่งสูงเกิน 0.5 จากกระแสข่าวในช่วงเช้าวันที่ 23 ก.พ. ทำให้เห็นว่าข่าวสารเชิงบวกเป็นปัจจัยหนุนสำคัญที่ช่วยผลักดันราคาได้




<img width="1400" height="700" alt="KTB BK" src="https://github.com/user-attachments/assets/3b71e29e-c65c-4f21-8cf7-a69bb0c250e1" />

ธนาคารกรุงไทย (KTB.BK): ในส่วนของ KTB มีความเคลื่อนไหวที่ค่อนข้างเสถียรแต่ยังคงรักษาทิศทางขาขึ้นได้ดี โดยราคาขยับจาก 32 บาท ไปยัง 34 บาท แม้กระแสข่าวสารที่ระบบตรวจพบจะมีความหลากหลายในเชิงเนื้อหามากกว่า แต่คะแนนความรู้สึกจากข่าวยังคงสอดคล้องกับการเคลื่อนไหวของราคาหุ้นกลุ่มธนาคารในภาพรวม แสดงให้เห็นถึงความสัมพันธ์เชิงบวกระหว่างอุตสาหกรรมและข่าวสาร
