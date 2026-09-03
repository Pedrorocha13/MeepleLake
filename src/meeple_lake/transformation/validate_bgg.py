import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_silver(df):
   
    checks = {
    "null_id": int(df["id"].isna().sum()),
    "duplicate_id": int(df["id"].duplicated().sum()),
    "null_name": int(df["name"].isna().sum()),
    "invalid_players": int((df["min_player"] > df["max_player"]).sum()),
    "invalid_playtime": int((df["min_play_time"] > df["max_play_time"]).sum()),
    "invalid_rating": int((~df["average_rating"].between(0, 10)).sum()),
    "invalid_year": int((~df["year"].between(1900, 2100)).sum()),
    }

    critical_checks = {
        "null_id":checks["null_id"],
        "duplicate_id": checks["duplicate_id"],
        "null_name": checks["null_name"],
    }

    for check, count in checks.items():
        logging.info(f"{check}: {count}")

    if any(count > 0 for count in critical_checks.values()):
        raise ValueError("Falha nas validações críticas da Silver")

    warning_checks = {
        "invalid_players": checks["invalid_players"],
        "invalid_playtime": checks["invalid_playtime"],
        "invalid_rating": checks["invalid_rating"],
        "invalid_year": checks["invalid_year"],
    }

    if any(count > 0 for count in warning_checks.values()):
        logging.warning("Foram encontradas validações problemáticas na Silver")

    return checks