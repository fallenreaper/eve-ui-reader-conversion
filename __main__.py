from base import *
import json

with open("sample.json") as fp:
  data = json.load(fp)

print("Entries: ", len(data))

u: UITreeNode = UITreeNode.fromJson(data)
print(u.dictEntriesOfInterest, u.pythonObjectAddress, u.pythonObjectTypeName)


ui = parseUserinterfaceFromUITree(parseUITreeWithDisplayRegionFromUITree(u))
print("Chat Window Stacks", ui.chatWindowStacks)

print("Dumping Chat windows and Usernames")
for cWindow in ui.chatWindowStacks:
  print("Window Name: ", cWindow.chatWindow.name)
  print("Users", [(x.name, x.standingIconHint) for x in cWindow.chatWindow.userlist.visibleUsers])