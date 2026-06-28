import pandas as pd
import joblib
import numpy as np
from detector.features import extract_features
from io import StringIO

model = joblib.load('model/logistic_model.pkl')
scaler = joblib.load('model/scaler.pkl')

data = """url,label
http://100.100.100.200/latest/meta-data/,SSRF
http://100.100.100.200/latest/meta-data/iam/,SSRF
http://192.0.0.192/latest/,SSRF
http://169.254.169.254/computeMetadata/v1/,SSRF
http://[::ffff:169.254.169.254]/,SSRF
http://[::ffff:7f00:1]/admin,SSRF
http://3232235777/admin,SSRF
http://2130706434/admin,SSRF
http://127.0.0.2/admin,SSRF
http://127.0.0.0/admin,SSRF
http://0.0.0.0:8080/admin,SSRF
http://127%2E0%2E0%2E1/admin,SSRF
http://169%2E254%2E169%2E254/,SSRF
http://internal.company.local/api,SSRF
http://corp.internal/admin,SSRF
http://intranet.local/dashboard,SSRF
http://192.168.0.0/network,SSRF
http://172.16.0.0/internal,SSRF
http://10.255.255.255/admin,SSRF
http://169.254.0.1/test,SSRF
http://169.254.254.254/test,SSRF
http://192.168.1.1:22/,SSRF
http://10.0.0.1:3306/,SSRF
http://172.16.0.1:6379/,SSRF
http://127.0.0.1:27017/,SSRF
https://anthropic.com/research,SAFE
https://openai.com/blog,SAFE
https://huggingface.co/models,SAFE
https://arxiv.org/abs/2024,SAFE
https://cybersecurity.mit.edu,SAFE
https://owasp.org/www-project-top-ten,SAFE
https://nvd.nist.gov/vuln,SAFE
https://portswigger.net/web-security,SAFE
https://tryhackme.com/dashboard,SAFE
https://hackerone.com/reports,SAFE
https://metadata.io/docs,SAFE
https://localhost.run/docs,SAFE
https://internal.io/about,SAFE
https://cloud.google.com/compute,SAFE
https://docs.aws.amazon.com/ec2,SAFE
https://api.stripe.com/v1/charges,SAFE
https://graph.facebook.com/me,SAFE
https://api.twitter.com/2/tweets,SAFE
https://registry.npmjs.org/react,SAFE
https://pypi.org/project/flask,SAFE
https://hub.docker.com/r/nginx,SAFE"""

df = pd.read_csv(StringIO(data))
correct_count = 0
print(f"{'URL':<45} | {'EXPECTED':<6} | {'PREDICTED'}")
print("-" * 70)

for _, row in df.iterrows():
    features = np.array(extract_features(row['url'])).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    predicted_label = "SSRF" if prediction[0] == 1 else "SAFE"
    result = "PASS" if predicted_label == row['label'] else "FAIL"
    if result == "PASS": correct_count += 1
    print(f"{row['url'][:45]:<45} | {row['label']:<6} | {predicted_label} ({result})")

print("-" * 70)
print(f"Accuracy: {(correct_count/len(df))*100:.2f}%")
