import json
from channels.generic.websocket import AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):# tạo chatsocket cho mục đích được yêu cầu
	async def connect(self):
		self.roomGroupName = "group_chat_gfg"
		await self.channel_layer.group_add(#tạo nhóm cho phòng trò chuyện và thêm nhóm
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):#xóa khỏi nhóm
		await self.channel_layer.group_discard(
			self.roomGroupName , 
			self.channel_layer 
		)
	async def receive(self, text_data): 
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message , 
				"username" : username ,
			})
	async def sendMessage(self , event) : 
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message ,"username":username}))
