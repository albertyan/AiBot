class EnvMode:
    DEV = "dev"
    PROD = "prod"
    def __init__(self):
        self.envMode = self.DEV
    
    def set_mode(self, mode: str):
        self.envMode = mode

env = EnvMode()

if __name__ == "__main__":
    # env = EnvMode()
    print(f"Current environment mode: {env.envMode}")
    # Example of setting the mode
    env.set_mode(EnvMode.PROD)
    print(f"Updated environment mode: {env.envMode}")