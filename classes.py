
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Set, Union


# Not Sure what this means at the common. Will need to check into it.
#  Wraping in a Try-Except in order to catch until I determine what it is.
try:
    CUSTOMKEYCODE = Common.EffectOnWindow.VirtualKeyCode
except:
    CUSTOMKEYCODE = None


UITreeNodeChild = None  # UITreeNode. # Reinit after to help class defs.


class UITreeNode(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def fromJson(data: Dict) -> object:
        x = UITreeNode(**data)
        _c = data.get("children")
        x.children = None if _c is None else [UITreeNodeChild.fromJson(x) for x in _c]
        return x

    origionalJson: Any
    pythonObjectAddress: str
    pythonObjectTypeName: str
    dictEntriesOfInterest: Dict[str, Any]
    children: Optional[List[UITreeNodeChild]]


# class UITreeNodeChild(Enum):
UITreeNodeChild = UITreeNode


class DisplayRegion(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    x: int
    y: int
    width: int
    height: int


# class ChildOfNodeWithDisplayRegion(Enum):
#     # UITreeNodeWithDisplayRegion # Reinit after to help class defs.



class UITreeNodeWithDisplayRegion(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNode
    children: Optional[List[Union[UITreeNode, Any]]]
    selfDisplayRegion: DisplayRegion
    totalDisplayRegion: DisplayRegion

ChildWithoutRegion = UITreeNode
ChildWithRegion = UITreeNodeWithDisplayRegion

#Defined a second time in order to init typings.
class UITreeNodeWithDisplayRegion(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNode
    children: Optional[List[Union[UITreeNode, UITreeNodeWithDisplayRegion]]]
    selfDisplayRegion: DisplayRegion
    totalDisplayRegion: DisplayRegion


# class ChildOfNodeWithDisplayRegion(Enum):
#     ChildWithRegion = UITreeNodeWithDisplayRegion
#     ChildWithoutRegion = UITreeNode


class Location2d:
    x: int
    y: int


class ColorComponents(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    a: int
    r: int
    g: int
    b: int



class ContextMenuEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    text: str


class ContextMenu(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[ContextMenuEntry]


class ShipUIModuleButton(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    slotUINode: UITreeNodeWithDisplayRegion
    isActive: Optional[bool]
    isHiliteVisible: bool
    rampRotationMilli: Optional[int]


class ModuleRows(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    top: List[ShipUIModuleButton]
    middle: List[ShipUIModuleButton]
    bottom: List[ShipUIModuleButton]


class Hitpoints(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    structure: int
    armor: int
    shield: int


class SquadronAbilityIcon(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    quantity: Optional[int]
    ramp_active: Optional[bool]


class SquadronUI(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    abilities: List[SquadronAbilityIcon]
    actionLabel: Optional[UITreeNodeWithDisplayRegion]


class SquadronsUI(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    squadrons: List[SquadronUI]


class ShipUICapacitorPmark(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    colorPercent: Optional[ColorComponents]


class ShipUICapacitor(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    pmarks: List[ShipUICapacitorPmark]
    levelFromPmarksPercent: Optional[int]


class ShipManeuverType(Enum):
    ManeuverWarp = 0,
    ManeuverJump = 1,
    ManeuverOrbit = 2,
    ManeuverApproach = 3


class ShipUIIndication(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    maneuverType: Optional[ShipManeuverType]


class ShipUI(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    capacitor: ShipUICapacitor
    hitpointsPercent: Hitpoints
    indication: Optional[ShipUIIndication]
    moduleButtons: List[ShipUIModuleButton]
    moduleButtonsRows: ModuleRows

    offensiveBuffButtonNames: List[str]
    squadronsUI: Optional[SquadronsUI]
    stopButton: Optional[UITreeNodeWithDisplayRegion]
    maxSpeedButton: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelIcons(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    search: Optional[UITreeNodeWithDisplayRegion]
    locationInfo: Optional[UITreeNodeWithDisplayRegion]
    route: Optional[UITreeNodeWithDisplayRegion]
    agentMissions: Optional[UITreeNodeWithDisplayRegion]
    dailyChallenge: Optional[UITreeNodeWithDisplayRegion]


class InfoPanelRouteRouteElementMarker(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelRoute(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    routeElementMarker: List[InfoPanelRouteRouteElementMarker]


class InfoPanelLocationInfoExpandedContent(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    currentStationName: Optional[str]


class InfoPanelLocationInfo(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    listSurroundingsButton: UITreeNodeWithDisplayRegion
    currentSolarSystemName: Optional[str]
    securityStatusPercent: Optional[int]
    expandedContent: Optional[InfoPanelLocationInfoExpandedContent]


class InfoPanelAgentMissionsEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion


class InfoPanelAgentMissions(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[InfoPanelAgentMissionsEntry]


class InfoPanelContainer(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    icons: Optional[InfoPanelIcons]
    infoPanelLocationInfo: Optional[InfoPanelLocationInfo]
    infoPanelRoute: Optional[InfoPanelRoute]
    infoPanelAgentMissions: Optional[InfoPanelAgentMissions]


class Target(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    barAndImageCont: Optional[UITreeNodeWithDisplayRegion]
    textsTopToBottom: List[str]
    isActiveTarget: bool
    assignedContainerNode: Optional[UITreeNodeWithDisplayRegion]
    assignedIcons: List[UITreeNodeWithDisplayRegion]


class OverviewWindowEntryCommonIndications(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    targeting: bool
    targetedByMe: bool
    isJammingMe: bool
    isWarpDisruptingMe: bool


class OverviewWindowEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    objectDistance: Optional[str]
    objectDistanceInMeters: Union[str, int]
    objectName: Optional[str]
    objectType: Optional[str]
    objectAlliance: Optional[str]
    iconSpriteColorPercent: Optional[ColorComponents]
    namesUnderSpaceObjectIcon: Set[str]
    bgColorFillsPercent: List[ColorComponents]
    rightAlignedIconsHints: List[str]
    commonIndications: OverviewWindowEntryCommonIndications


class ScrollControls(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    scrollHandle: Optional[UITreeNodeWithDisplayRegion]


class OverviewWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    entriesHeaders: List[Union[str, UITreeNodeWithDisplayRegion]]
    entries: List[OverviewWindowEntry]
    scrollControls: Optional[ScrollControls]


class SelectedItemWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    orbitButton: Optional[UITreeNodeWithDisplayRegion]


class FittingWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion


class MarketOrdersWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion


class SurveyScanWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    scanEntries: List[UITreeNodeWithDisplayRegion]


class RepairShopWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    items: List[UITreeNodeWithDisplayRegion]
    repairItemButton: Optional[UITreeNodeWithDisplayRegion]
    pickNewItemButton: Optional[UITreeNodeWithDisplayRegion]
    repairAllButton: Optional[UITreeNodeWithDisplayRegion]


class CharacterSheetWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    skillGroups: List[UITreeNodeWithDisplayRegion]


class Expander(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    texturePath: Optional[str]
    isExpanded: Optional[bool]


class DronesWindowDroneGroupHeader(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    expander: Expander
    quantityFromTitle: Optional[int]


class DronesWindowEntryGroupStructure(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    header: DronesWindowDroneGroupHeader
    children: List[Any]  # DronesWindowEntry


class DronesWindowEntryDroneStructure(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]
    hitpointsPercent: Optional[Hitpoints]


# class DronesWindowEntry(Enum):
DronesWindowEntryGroup = DronesWindowEntryGroupStructure
DronesWindowEntryDrone = DronesWindowEntryDroneStructure

class DronesWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    droneGroups: List[DronesWindowEntryGroupStructure]
    droneGroupInBay: Optional[DronesWindowEntryGroupStructure]
    droneGroupInLocalSpace: Optional[DronesWindowEntryGroupStructure]


class ProbeScanResult(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    textsLeftToRight: List[str]
    cellsTexts: Dict[str, str]
    warpButton: Optional[UITreeNodeWithDisplayRegion]


class ProbeScannerWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    scanResults: List[ProbeScanResult]


class DirectionalScannerWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    scrollNode: Optional[UITreeNodeWithDisplayRegion]
    scanResults: List[UITreeNodeWithDisplayRegion]


class StationWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    undockButton: Optional[UITreeNodeWithDisplayRegion]
    abortUndockButton: Optional[UITreeNodeWithDisplayRegion]

InventoryWindowLeftTreeEntryChild: Any = None

class InventoryWindowLeftTreeEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    toggleBtn: Optional[UITreeNodeWithDisplayRegion]
    selectRegion: Optional[UITreeNodeWithDisplayRegion]
    text: str
    children: List[InventoryWindowLeftTreeEntryChild]

InventoryWindowLeftTreeEntryChild = InventoryWindowLeftTreeEntry

class InventoryWindowCapacityGauge(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    used: int
    maximum: Optional[int]
    selected: Optional[int]


class Items(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    items: List[UITreeNodeWithDisplayRegion]


class InventoryItemsView(Enum):
    InventoryItemsListView = Items
    InventoryItemsNotListView = Items


class Inventory(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    itemsView: Optional[InventoryItemsView]
    scrollControls: Optional[ScrollControls]


class InventoryWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    leftTreeEntries: List[InventoryWindowLeftTreeEntry]
    subCaptionLabelText: Optional[str]
    selectedContainerCapacityGauge: Optional[Union[str,
                                                   InventoryWindowCapacityGauge]]
    selectedContainerInventory: Optional[Inventory]
    buttonToSwitchToListView: Optional[UITreeNodeWithDisplayRegion]


class ChatUserEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    standingIconHint: Optional[str]


class ShortCut(NamedTuple):
    text: str
    parseResult: Optional[Union[str, List[CUSTOMKEYCODE]]]


class ChatWindowUserlist(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    visibleUsers: List[ChatUserEntry]
    scrollControls: Optional[ScrollControls]


class ChatWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    name: Optional[str]
    userlist: Optional[ChatWindowUserlist]


class ChatWindowStack(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    chatWindow: Optional[ChatWindow]


class OptimalRange(NamedTuple):
    asString: str
    inMeteres: Union[str, int]


class ModuleButtonTooltip(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    shortcut: Optional[ShortCut]
    optimalRange: Optional[OptimalRange]


class ParsedTime(NamedTuple):
    hour: int
    minute: int


class OffsetWidth(NamedTuple):
    offset: int
    width: int


class NeocomClock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    text: str
    ParsedTime: Union[str, ParsedTime]


class Neocom(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    iconInventory: Optional[UITreeNodeWithDisplayRegion]
    clock: Optional[NeocomClock]


class AgentConversationWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion


class BookmarkLocationWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    submitButton: Optional[UITreeNodeWithDisplayRegion]
    cancelButton: Optional[UITreeNodeWithDisplayRegion]


class ButtonTuples(NamedTuple):
    uiNode: UITreeNodeWithDisplayRegion
    maintext: Optional[str]


class MessageBox(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    buttons: List[ButtonTuples]


class FleetWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    fleetMembers: List[UITreeNodeWithDisplayRegion]


class WatchListPanel(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class StandaloneBookmarkWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    entries: List[UITreeNodeWithDisplayRegion]


class KeyActivationWindow(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiNode: UITreeNodeWithDisplayRegion
    activateButton: Optional[UITreeNodeWithDisplayRegion]


class ParsedUserInterface(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    uiTree: UITreeNodeWithDisplayRegion
    contextMenus: List[ContextMenu]
    shipUI: Optional[ShipUI]
    targets: List[Target]
    infoPanelContainer: Optional[InfoPanelContainer]
    overviewWindow: Optional[OverviewWindow]
    selectedItemWindow: Optional[SelectedItemWindow]
    dronesWindow: Optional[DronesWindow]
    fittingWindow: Optional[FittingWindow]
    probeScannerWindow: Optional[ProbeScannerWindow]
    directionalScannerWindow: Optional[DirectionalScannerWindow]
    stationWindow: Optional[StationWindow]
    inventoryWindows: List[InventoryWindow]
    chatWindowStacks: List[ChatWindowStack]
    agentConversationWindows: List[AgentConversationWindow]
    marketOrdersWindow: Optional[MarketOrdersWindow]
    surveyScanWindow: Optional[SurveyScanWindow]
    bookmarkLocationWindow: Optional[BookmarkLocationWindow]
    repairShopWindow: Optional[RepairShopWindow]
    characterSheetWindow: Optional[CharacterSheetWindow]
    fleetWindow: Optional[FleetWindow]
    watchListPanel: Optional[WatchListPanel]
    standaloneBookmarkWindow: Optional[StandaloneBookmarkWindow]
    moduleButtonTooltip: Optional[ModuleButtonTooltip]
    neocom: Optional[Neocom]
    messageBoxes: List[MessageBox]
    layerAbovemain: Optional[UITreeNodeWithDisplayRegion]
    keyActivationWindow: Optional[KeyActivationWindow]
