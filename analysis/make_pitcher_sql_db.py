# SYSTEM IMPORTS
import sqlite3
import pandas as pd
import os

# PYTHON PROJECT IMPORTS
# USERid_SESSIONid_HEIGHT_WEIGHT_PITCHNUMBER_PITCHTYPE_PITCHSPEED.c3d

base_path = str = r"D:\baseball_projects\\openbiomechanics\\baseball_pitching\\data"

def main():
    con = sqlite3.connect(os.path.join(base_path, "openbiomechanics_pitching_database.db"))
    cur = con.cursor()

    res = {x[0] for x in cur.execute("SELECT name FROM sqlite_master").fetchall()}
    print(res)

    if "pitcher" not in res:
        # create mouse table
        cur.execute(
    """CREATE TABLE pitcher(
        id varchar(6),
        weight varchar(8),
        height varchar(8),
        p_throws varchar(1),
        level varchar(20),
        PRIMARY KEY (id)
    )"""
        )
        con.commit()

    if "pitch" not in res:
        # create inv aligned table
        cur.execute(
    """CREATE TABLE pitch(
        pitcher_id varchar(6),
        session varchar(4),
        pitch_num INTEGER,
        pitch_type varchar(10),
        pitch_speed varchar(8),
        full_c3d varchar(1024),
        energy_flow varchar(1024),
        force_plate varchar(1024),
        forces_movement varchar(1024),
        joint_angles varchar(1024),
        joint_velos varchar(1024),
        landmarks varchar(1024),
        poi_metrics varchar(1024),
        PRIMARY KEY (pitcher_id, session, pitch_num)
        FOREIGN KEY (pitcher_id) REFERENCES pitcher(id)
    )"""
        )
        con.commit()
        
    res = {x[0] for x in cur.execute("SELECT name FROM sqlite_master").fetchall()}
    print(f"tables in this database: {res}")
    

if __name__ == "__main__":
	main()

