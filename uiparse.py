
from classes import *
def getDisplayText(uiNode: UITreeNode) -> Optional[str]:
  _keys = ['_setText', '_text']
  result: List[str] = []
  for key in _keys:
    if key in uiNode.dictEntriesOfInterest:
      result.append(uiNode.dictEntriesOfInterest[key])
  result.sort(lambda a,b: len(a) > len(b))
  return result[0] if result is not None else None

# getDisplayText : EveOnline.MemoryReading.UITreeNode -> Maybe String
# getDisplayText uiNode =
#     [ "_setText", "_text" ]
#         |> List.filterMap
#             (\displayTextPropertyName ->
#                 uiNode.dictEntriesOfInterest
#                     |> Dict.get displayTextPropertyName
#                     |> Maybe.andThen (Json.Decode.decodeValue Json.Decode.string >> Result.toMaybe)
#             )
#         |> List.sortBy (String.length >> negate)
#         |> List.head