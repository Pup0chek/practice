import redis


class Redis:
    def __init__(self):
        self.client = redis.StrictRedis(host="localhost", port="6379", db=0)

    def create_record(self,key:str, value:str):
        self.client.set(key, value)
        return {"message": "success"}

    def read_record(self, key:str):
        value = self.client.get(key)
        return {"message": value.decode('utf-8')}

    def delete_record(self, key):
        self.client.delete(key)
        return {"message":"success"}

    def if_exist(self, key):
        exists = self.client.exists(key)
        return {"message": f"{bool(exists)}"}

def main():
    red = Redis()
    #print(red.create_record('name', 'lia'))
    print(red.read_record('string'))
    print(red.if_exist('string'))

if __name__ == "__main__":
    main()




