import os
import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import time
class SkinConditionNNClassifier:
    def __init__(self, csv_path, image_folder):
        self.csv_path = csv_path
        self.image_folder = image_folder
        self.load_data()
        self.prepare_data()

    def load_data(self):
        # قراءة ملف CSV
        data = pd.read_csv(self.csv_path)
        # الأعمدة المهمة: image_id (لربط الصور) و dx (الفئات)
        images = []
        labels = []
        i = 0
        for _, row in data.iterrows():
            i += 1
            print(i)
            image_id = row["image_id"]
            label = row["dx"]
            image_path = os.path.join(self.image_folder, f"{image_id}.jpg")
            try:
                # قراءة الصورة وتحويلها إلى ألوان وتغيير الحجم
                img = cv2.imread(image_path, cv2.IMREAD_COLOR)
                if img is None:
                    continue  # تخطي الصورة إذا كانت غير موجودة أو تالفة
                img = cv2.resize(img, (128, 128))  # تغيير الحجم إلى 128x128
                images.append(img)  # إضافة الصورة بالشكل الصحيح
                labels.append(label)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        # تحويل الصور والتسميات إلى NumPy arrays
        self.images = np.array(images) / 255.0  # Normalization
        self.labels = np.array(labels)

    def prepare_data(self):
        # تحويل labels إلى قيم عددية (Label Encoding)
        label_encoder = LabelEncoder()
        self.labels_encoded = label_encoder.fit_transform(self.labels)
        # تحويل labels إلى One-Hot Encoding
        self.labels_onehot = to_categorical(self.labels_encoded)
        # حفظ الفئات وفهرستها
        self.label_mapping = {idx: label for idx, label in enumerate(label_encoder.classes_)}
        # تقسيم البيانات إلى تدريب واختبار
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.images, self.labels_onehot, test_size=0.2, random_state=42
        )

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(128, 128, 3)))  # طبقة تلافيفية
        model.add(MaxPooling2D(pool_size=(2, 2)))  # طبقة تجميعية
        model.add(Conv2D(64, (3, 3), activation="relu"))  # طبقة تلافيفية أخرى
        model.add(MaxPooling2D(pool_size=(2, 2)))  # طبقة تجميعية أخرى
        model.add(Flatten())  # Flatten لتحويل الأبعاد إلى شكل مسطح قبل الطبقات الكثيفة
        model.add(Dense(128, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.label_mapping), activation="softmax"))  # الطبقة النهائية
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        self.model = model

    def train_and_evaluate(self, epochs=20, batch_size=32):
        # استخدام ImageDataGenerator لتوسيع البيانات
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        # تدريب النموذج باستخدام توسيع البيانات
        history = self.model.fit(
            datagen.flow(self.X_train, self.y_train, batch_size=batch_size),
            validation_data=(self.X_test, self.y_test),
            epochs=epochs
        )
        # تقييم النموذج
        loss, accuracy = self.model.evaluate(self.X_test, self.y_test)
        print(f"Test Loss: {loss}")
        print(f"Test Accuracy: {accuracy}")
        # رسم دقة التدريب ودقة التحقق
        plt.plot(history.history["accuracy"], label="Training Accuracy")
        plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
        plt.xlabel("Epochs")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.title("Training vs Validation Accuracy")
        plt.show()
        # رسم الخسارة
        plt.plot(history.history["loss"], label="Training Loss")
        plt.plot(history.history["val_loss"], label="Validation Loss")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()
        plt.title("Training vs Validation Loss")
        plt.show()

    def predict(self, image_path):
        # قراءة الصورة بنفس طريقة معالجة البيانات
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)  # قراءة الصورة بالألوان
        img = cv2.resize(img, (128, 128))  # تغيير الحجم إلى 128x128
        img = img / 255.0  # Normalization
        img = img.reshape(1, 128, 128, 3)  # إعادة تشكيل الصورة لتطابق المدخل المطلوب للنموذج
        # توقع الفئة
        probabilities = self.model.predict(img)
        predicted_class = np.argmax(probabilities)
        return self.label_mapping[predicted_class]

x=time.time()
# مثال على الاستخدام:
csv_path = "HAM10000_metadata.csv"  # المسار إلى ملف CSV
image_folder = "images"  # المسار إلى مجلد الصور

classifier = SkinConditionNNClassifier(csv_path, image_folder)
classifier.build_model()
classifier.train_and_evaluate(epochs=20, batch_size=32)
classifier.train_and_evaluate(epochs=5, batch_size=32)

# إدخال صورة جديدة
# image_path = "ISIC_0031783.jpg"  # هنا تقوم بإدخال مسار الصورة الجديدة
# predicted_condition = classifier.predict(image_path)
image_path = "AKIEC.jpg"  # ضع مسار الصورة هنا
predicted_condition = classifier.predict(image_path)
print(f"The predicted skin condition is: {predicted_condition}")
print(f"all time =  {(time.time()-x)/60}")
# print(f"predicted discease: {predicted_condition}")
input("press any key ")
