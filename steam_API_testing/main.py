# --- DEPENDENCIES --- #
# pip install requests beautifulsoup4
# python 3.7+

# --- TESTING --- #
# app ids of popular games
# 730: CS:GO / CS2
# 440: TF2
# 570: Dota 2

# --- CODE --- #
import requests
from bs4 import BeautifulSoup



def get_app_details(appid):
    # get JSON info for the given appid
    url = f"https://store.steampowered.com/api/appdetails"
    parameters = {"appids": appid, "currency": "EUR", "l": "english"}
    response = requests.get(url, params=parameters)
    response.raise_for_status()  
    if response.json().get(appid, {}).get("success") == True:
        return response.json()[appid]["data"]
    else:
        return "Error: App not found"
    
def get_current_players(appid):
    # calls Steam Web API GetNumberOfCurrentPlayers for the given appid
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    params = {"appid": appid}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    j = resp.json()
    return j.get("response", {}).get("player_count")

def parse_requirements(html_block):
    # parse a Steam-style <ul><li><strong>Key:</strong> Value</li>…</ul> (or similar) into a list of bullet strings like "• Key: Value" for better readability
    if not html_block:
        return []
    soup = BeautifulSoup(html_block, "html.parser")
    bullets = []
    for li in soup.find_all("li"):
        strong = li.find("strong")
        if strong:
            label = strong.get_text(strip=True).rstrip(":")
            strong.extract()
            value = li.get_text(strip=True)
            bullets.append(f"• {label}: {value}")
        else:
            text = li.get_text(strip=True)
            if text:
                bullets.append(f"• {text}")
    if not bullets:
        text = soup.get_text(separator="\n").strip()
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if len(lines) >= 2 and lines[0].rstrip(":").lower() in ("minimum", "recommended"):
            lines = lines[1:]
        for line in lines:
            if ":" in line:
                bullets.append(f"• {line}")
            else:
                bullets.append(f"• {line}")
    return bullets

def show_game_info(appid):
    # 1) get Store API details
    data = get_app_details(appid)
    if not data:
        print(f"No data found for AppID {appid}.")
    # 2) get current players
    current_players = get_current_players(appid)
    # 3) name and date
    name = data.get("name", "—")
    release_date = data.get("release_date", {}).get("date", "—")
    # 4) reviews
    reviews = data.get("recommendations", {}).get("total", 0)
    # pricing
    price_overview = data.get("price_overview")
    if price_overview:
        final = price_overview.get("final")   # in cents
        initial = price_overview.get("initial")
        currency = price_overview.get("currency")
        discount = price_overview.get("discount_percent")
        # conversion from cents to dollars
        final_price = f"{final / 100:.2f} {currency}" if final is not None else "Free"
        if discount and discount > 0:
            original_price = f"{initial / 100:.2f} {currency}"
        else:
            original_price = None
    else:
        final_price = "Free" if data.get("is_free") else "N/A"
        original_price = None
        discount = 0
    # developer / publisher
    developers = ", ".join(data.get("developers", [])) or "—"
    publishers = ", ".join(data.get("publishers", [])) or "—"
    # genres
    genres = ", ".join([g.get("description", "") for g in data.get("genres", [])]) or "—"
    # achievements
    total_achievements = data.get("achievements", {}).get("total", 0)
    # platforms
    platforms = data.get("platforms", {})
    platform_list = [name.capitalize() for name, supported in platforms.items() if supported]
    platform_str = ", ".join(platform_list) if platform_list else "—"
    # requirements
    pc_reqs = data.get("pc_requirements", {})
    min_req_html = pc_reqs.get("minimum")
    rec_req_html = pc_reqs.get("recommended")
    min_bullets = parse_requirements(min_req_html)
    rec_bullets = parse_requirements(rec_req_html)

    # PRINT SUMMARY
    print(f"# --- Game Details Summary for AppID {appid} --- #\n")
    print(f"Name:           {name}")
    print(f"Release Date:   {release_date}")
    print(f"Developer(s):   {developers}")
    print(f"Publisher(s):   {publishers}")
    print(f"Genre(s):       {genres}")
    print(f"Price:          {final_price}", end="")
    if original_price:
        print(f" (Original: {original_price}, Discount: {discount}%)")
    else:
        print()
    print(f"Reviews:        {reviews:,} total")
    # player stats
    if current_players is not None:
        print(f"Current Players:       {current_players:,}")
    else:
        print("Current Players:       0")
    # achievements
    if total_achievements > 0:
        print(f"Total Achievements:    {total_achievements}")
    else:
        print("Total Achievements:    0")
    print()
    # platforms
    print(f"Platforms: {platform_str}")
    # requirements
    if min_bullets:
        print("Minimum PC Requirements:")
        for b in min_bullets:
            print(f"  {b}")
    else:
        print("Minimum PC Requirements: N/A")
    print()
    if rec_bullets:
        print("Recommended PC Requirements:")
        for b in rec_bullets:
            print(f"  {b}")
    else:
        print("Recommended PC Requirements: N/A")
    print()

def main():
    appid = input("Enter AppID of the app you want to analyze: ")
    if not appid.isdigit():
        print("Invalid AppID. Please enter a valid number.")
        return
    
    print(f"Fetching data for AppID {appid}...\n")

    show_game_info(appid)


# --- MAIN PROGRAM LOOP --- #
if __name__ == "__main__":
    main()
