from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def RandomAgent()->dict:
    """
    Afin d'éviter de se faire ban en tant que Robot, nous générons des user agent aléatoirement grâce a la bibliothèque random-user-agent

    Returns:
        dict: retourne un user agent parmi la liste de user agent trouvé sur le Web
    """
    # 
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1500)
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': user_agent}
    return headers