# compiler_task_2
Check if the grammer is simple or not
![WhatsApp Image 2024-12-15 at 01 09 46_c3859c92](https://github.com/user-attachments/assets/04df0f55-7bb4-47e9-9355-54f8f153a23f)
![WhatsApp Image 2024-12-15 at 01 09 45_23a89f6b](https://github.com/user-attachments/assets/14ec493b-2caa-406a-937c-c390eb59badf)



# تحليل ملف التقاط الشبكة واستخراج العلم

## مقدمة

تم تقديم ملف التقاط شبكة (`capture.pcapng`) مع طلب لتحليل الحركة واستخراج علم (flag) مخفي بداخله. يوضح هذا المستند الخطوات التفصيلية التي تم اتخاذها لتحليل الملف والعثور على العلم.

## الخطوات المتبعة

### 1. التحليل الأولي وتثبيت الأدوات

- **فحص البروتوكولات:** تم استخدام أداة `tshark` لفحص البروتوكولات المستخدمة في ملف الالتقاط.
  ```bash
  tshark -r /home/ubuntu/upload/capture.pcapng -q -z io,phs
  ```
  أظهر التحليل وجود 8 إطارات TCP، وواحدة منها تحتوي على بيانات (payload).
- **تثبيت الأدوات:** تم تثبيت الأدوات اللازمة للتحليل مثل `tshark` و `binutils` (التي تحتوي على `strings`) و `foremost` و `binwalk`.
  ```bash
  sudo apt-get update && sudo apt-get install -y tshark binutils foremost binwalk
  ```

### 2. استخراج بيانات تدفق TCP

- **استخراج النص:** تم استخراج تدفق TCP الأول (stream 0) بصيغة ASCII لمحاولة العثور على العلم كنص واضح.
  ```bash
  tshark -r /home/ubuntu/upload/capture.pcapng -q -z follow,tcp,ascii,0 > /home/ubuntu/tcp_stream_0.txt
  ```
  لم يظهر أي علم واضح في النص المستخرج.
- **استخراج الهيكس:** تم استخراج نفس التدفق بصيغة Hexadecimal لفحص البيانات الثنائية.
  ```bash
  tshark -r /home/ubuntu/upload/capture.pcapng -q -z follow,tcp,hex,0 > /home/ubuntu/tcp_stream_0_hex.txt
  ```

### 3. محاولات أولية للعثور على العلم

- **البحث عن كلمات مفتاحية:** تم استخدام `grep` للبحث عن الكلمات الشائعة مثل `flag` أو `ctf` في النص المستخرج، لكن لم يتم العثور على شيء.
  ```bash
  grep -i 'flag\|ctf' /home/ubuntu/tcp_stream_0.txt
  ```
- **استخراج السلاسل النصية:** تم استخراج الحمولة (payload) الوحيدة من الحزمة التي تحتوي على بيانات، ثم تم استخدام أداة `strings` لمحاولة العثور على أي نصوص مخفية.
  ```bash
  tshark -r /home/ubuntu/upload/capture.pcapng -Y "tcp.stream eq 0 && data" -T fields -e data > /home/ubuntu/raw_payload.hex
  cat /home/ubuntu/raw_payload.hex | xxd -r -p | strings
  ```
  النتيجة الوحيدة كانت `xCEAf`، والتي لم تكن العلم الصحيح.

### 4. استخدام أدوات التحليل الجنائي

- **Foremost:** تم استخدام أداة `foremost` لمحاولة استخراج أي ملفات مضمنة داخل ملف الالتقاط.
  ```bash
  foremost -i /home/ubuntu/upload/capture.pcapng -o /home/ubuntu/foremost_output
  ```
  لم يتم استخراج أي ملفات.
- **Binwalk:** تم استخدام أداة `binwalk` للبحث عن توقيعات ملفات معروفة أو بيانات قابلة للاستخراج.
  ```bash
  binwalk /home/ubuntu/upload/capture.pcapng
  ```
  لم يتم العثور على أي نتائج.

### 5. تحليل الحمولة الثنائية وتفكيك الشيفرة

- **استخراج الحمولة الخام:** تم استخراج جميع الحمولات الخام من الملف للتأكد من عدم تفويت أي بيانات.
  ```bash
  tshark -r /home/ubuntu/upload/capture.pcapng -T fields -e data > /home/ubuntu/all_raw_payload.hex
  ```
- **محاولات فك التشفير (XOR و Base64):** تم كتابة وتشغيل برنامج بايثون (`decode_payload.py`) لمحاولة فك تشفير الحمولة باستخدام XOR بجميع المفاتيح الممكنة (0-255) ومحاولة فك ترميز Base64. لم تسفر هذه المحاولات عن نتائج ذات معنى.
- **تفكيك الشيفرة (Disassembly):** نظرًا لأن البيانات لم تكن نصًا عاديًا أو ملفًا مضمنًا، تم التعامل مع الحمولة على أنها شيفرة برمجية محتملة. تم تحويل الحمولة من Hex إلى ثنائي ثم تم تفكيكها باستخدام `objdump`.
  ```bash
  cat /home/ubuntu/all_raw_payload.hex | xxd -r -p > /home/ubuntu/payload.bin
  objdump -D -b binary -m i386:x86-64 /home/ubuntu/payload.bin > /home/ubuntu/disassembly.txt
  ```

### 6. تحليل الشيفرة المفككة واستخراج العلم

- **فهم الخوارزمية:** أظهر تحليل ملف `disassembly.txt` وجود شيفرة برمجية تقوم بتحميل جزأين من البيانات في الذاكرة ثم تقوم بتنفيذ عملية XOR بينهما بايت ببايت داخل حلقة تكرارية (loop).
- **استخراج البيانات المشفرة:** تم استخراج القيم السداسية عشرية (hex values) للبيانات المشفرة مباشرة من تعليمات `mov` في الشيفرة المفككة.
- **محاكاة عملية XOR:** تم كتابة برنامج بايثون (`solve_xor.py`) لمحاكاة عملية XOR التي تقوم بها الشيفرة البرمجية على البيانات المستخرجة.
  ```python
  #!/usr/bin/env python3
  import binascii

  # Data extracted from disassembly
  chunk1_hex = "260c69c77a9722bb" + "78434541" + "794d" + "00"
  chunk2_hex = "606008a001d00ff0" + "3d0d0a03" + "3030" + "00"

  chunk1 = binascii.unhexlify(chunk1_hex)
  chunk2 = binascii.unhexlify(chunk2_hex)

  length = min(len(chunk1), len(chunk2))

  result = bytearray(length)
  for i in range(length):
      result[i] = chunk1[i] ^ chunk2[i]

  try:
      flag = result.decode("ascii")
      print(f"Decoded flag: {flag}")
  except UnicodeDecodeError as e:
      print(f"Could not decode result as ASCII: {e}")
      print(f"Result (bytes): {result}")
  ```
- **تشغيل البرنامج:** عند تشغيل البرنامج، تم فك تشفير البيانات بنجاح.
  ```bash
  python3.11 /home/ubuntu/solve_xor.py
  ```
  الناتج كان: `Decoded flag: Flag{G-KENOBI}\x00`

## العلم النهائي

العلم الصحيح الذي تم استخراجه هو:

`Flag{G-KENOBI}`

