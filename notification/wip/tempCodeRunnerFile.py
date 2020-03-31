drivers = requests.post("http://localhost:88/usertype", json={"user_type": "driver"})
print(drivers)