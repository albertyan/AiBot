from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class AutoGreetingConfig(BaseModel):
    enabled: bool = False
    greetingGroupId: Optional[str] = None

class FileRecognitionConfig(BaseModel):
    enabled: bool = False
    fileTypes: List[str] = Field(default_factory=list)
    filePath: str = ""

    @field_validator('fileTypes')
    @classmethod
    def validate_file_types(cls, v):
        valid_types = {"word", "pdf", "excel", "image"}
        # Filter invalid types silently or raise error? 
        # The previous implementation filtered silently. Let's keep it consistent but cleaner.
        # However, Pydantic validators usually validate and return or raise.
        # If we want to filter, we can do it here.
        return [t for t in v if t in valid_types]

class WhitelistConfig(BaseModel):
    enabled: bool = False
    names: str = ""
    list: List[str] = Field(default_factory=list)

class CommonConfig(BaseModel):
    groupAtOnly: bool = False
    colleagueNamesToIgnore: str = ""
    filterWords: List[str] = Field(default_factory=list)
    autoGreeting: AutoGreetingConfig = Field(default_factory=AutoGreetingConfig)
    fileRecognition: FileRecognitionConfig = Field(default_factory=FileRecognitionConfig)
    whitelist: WhitelistConfig = Field(default_factory=WhitelistConfig)

class StaffAgent(BaseModel):
    id: Optional[str] = None
    name: str
    agentId: str
    chatType: Optional[str] = "single"
    selectedTags: List[str] = Field(default_factory=lambda: ["untagged"])
    keywords: List[str] = Field(default_factory=list)
    enabled: bool = True

class AgentId(BaseModel):
    agent_id: str

class UpdateEnableStatus(BaseModel):
    agent_id: str
    enabled: bool

class MonitorControl(BaseModel):
    enabled: bool

class WeChatSession(BaseModel):
    id: str = ""
    name: str
    count: int = 0
    last_message: str = ""
    last_time: str = ""
    is_top: bool = False
    raw_content: str = ""
    is_group: bool = False
    source: str = ""
