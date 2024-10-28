import sqlite3
import pandas as pd
import os
import re

base_path = r"D:\baseball_projects\openbiomechanics\baseball_pitching\data"
full_sig_path = os.path.join(base_path, "full_sig")  # Path to full_sig subdirectory
c3d_path = os.path.join(base_path, "c3d")  # Path to c3d subdirectory
poi_path = os.path.join(base_path, "poi")  # Path to poi_metrics subdirectory

def insert_pitcher_data(cur, pitcher_id, weight, height, level, p_throws):
    """Insert data into the pitcher table if it does not exist."""
    cur.execute("""
    INSERT OR IGNORE INTO pitcher (id, weight, height, level, p_throws)
    VALUES (?, ?, ?, ?, ?)
    """, (pitcher_id, weight, height, level, p_throws))

def insert_pitch_data(cur, pitcher_id, session, pitch_num, pitch_type, pitch_speed, full_c3d, energy_flow, force_plate, forces_movement, joint_angles, joint_velos, landmarks, poi_metrics):
    """Insert data into the pitch table. Converts tuples to strings for storage."""
    cur.execute("""
    INSERT OR IGNORE INTO pitch (
        pitcher_id, session, pitch_num, pitch_type, pitch_speed, full_c3d, energy_flow,
        force_plate, forces_movement, joint_angles, joint_velos, landmarks, poi_metrics
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (pitcher_id, session, pitch_num, pitch_type, pitch_speed, full_c3d, str(energy_flow), str(force_plate), str(forces_movement), str(joint_angles), str(joint_velos), str(landmarks), str(poi_metrics)))

def load_data():
    # Load metadata and other CSVs only once at the beginning
    metadata_df = pd.read_csv(os.path.join(base_path, "metadata.csv"))
    energy_flow_path = os.path.join(full_sig_path, "energy_flow", "energy_flow.csv")
    force_plate_path = os.path.join(full_sig_path, "force_plate", "force_plate.csv")
    forces_moments_path = os.path.join(full_sig_path, "forces_moments", "forces_moments.csv")
    joint_angles_path = os.path.join(full_sig_path, "joint_angles", "joint_angles.csv")
    joint_velos_path = os.path.join(full_sig_path, "joint_velos", "joint_velos.csv")
    landmarks_path = os.path.join(full_sig_path, "landmarks", "landmarks.csv")
    poi_metrics_path = os.path.join(poi_path, "poi_metrics.csv")

    # Load DataFrames
    energy_flow_df = pd.read_csv(energy_flow_path)
    force_plate_df = pd.read_csv(force_plate_path)
    forces_moments_df = pd.read_csv(forces_moments_path)
    joint_angles_df = pd.read_csv(joint_angles_path)
    joint_velos_df = pd.read_csv(joint_velos_path)
    landmarks_df = pd.read_csv(landmarks_path)
    poi_metrics_df = pd.read_csv(poi_metrics_path)

    # Establish database connection
    con = sqlite3.connect(os.path.join(base_path, "openbiomechanics_pitching_database.db"))
    cur = con.cursor()

    # Iterate over pitcher folders in the c3d directory
    for pitcher_folder in os.listdir(c3d_path):
        if os.path.isdir(os.path.join(c3d_path, pitcher_folder)) and re.match(r"\d{6}", pitcher_folder):
            pitcher_id = pitcher_folder.lstrip('0')  # Remove leading zeros

            # Retrieve metadata for pitcher
            pitcher_metadata = metadata_df[metadata_df['user'] == int(pitcher_id)]
            if pitcher_metadata.empty:
                continue

            weight = pitcher_metadata['session_mass_kg'].values[0]
            height = pitcher_metadata['session_height_m'].values[0]
            level = pitcher_metadata['playing_level'].values[0]

            # Insert pitcher data using placeholder for p_throws (will be updated later)
            insert_pitcher_data(cur, pitcher_id, weight, height, level, None)
            
            # Gather and sort pitch files by pitch_num in each pitcher folder
            pitch_files = []
            for pitch_file in os.listdir(os.path.join(c3d_path, pitcher_folder)):
                match = re.match(r"(\w+)_(\w+)_(\d+)_(\d+)_(\d+)_(\w+)_(\d{3})\.csv", pitch_file)
                if match:
                    user, session, _, _, pitch_num, pitch_type, pitch_speed_raw = match.groups()
                    pitch_speed = float(pitch_speed_raw[:-1] + '.' + pitch_speed_raw[-1])
                    pitch_files.append((int(pitch_num), pitch_file, session, pitch_type, pitch_speed))

            # Sort by pitch_num
            pitch_files.sort()

            # Map sorted pitch files to consecutive pitch_num order
            for ordered_pitch_num, (original_pitch_num, pitch_file, session, pitch_type, pitch_speed) in enumerate(pitch_files, start=1):
                full_c3d = os.path.join(c3d_path, pitcher_folder, pitch_file)
                
                # Format session_pitch and remove leading zeros
                session_pitch = f"{session}_{ordered_pitch_num}".lstrip('0')
                
                # Retrieve p_throws based on session_pitch from poi_metrics
                p_throws_row = poi_metrics_df[poi_metrics_df['session_pitch'] == session_pitch]
                p_throws = p_throws_row['p_throws'].values[0] if not p_throws_row.empty else None

                # Update p_throws for the pitcher table entry if it's None
                cur.execute("""
                UPDATE pitcher SET p_throws = ?
                WHERE id = ? AND p_throws IS NULL
                """, (p_throws, pitcher_id))

                # Insert pitch data using the ordered pitch number for correct matching
                insert_pitch_data(cur, pitcher_id, session, ordered_pitch_num, pitch_type, pitch_speed, full_c3d,
                                  select_rows(energy_flow_path, energy_flow_df, session_pitch),
                                  select_rows(force_plate_path, force_plate_df, session_pitch),
                                  select_rows(forces_moments_path, forces_moments_df, session_pitch),
                                  select_rows(joint_angles_path, joint_angles_df, session_pitch),
                                  select_rows(joint_velos_path, joint_velos_df, session_pitch),
                                  select_rows(landmarks_path, landmarks_df, session_pitch),
                                  select_rows(poi_metrics_path, poi_metrics_df, session_pitch))

    # Commit and close connection
    con.commit()
    con.close()

def select_rows(csv_path, df, session_pitch):
    """Select the first and last rows containing session_pitch and return them as a string tuple."""
    try:
        rows_with_session_pitch = df[df['session_pitch'] == session_pitch].index
        if not rows_with_session_pitch.empty:
            first_row = rows_with_session_pitch[0]
            last_row = rows_with_session_pitch[-1]
            return str((csv_path, first_row, last_row))  # Convert tuple to string for database storage
        else:
            return None  # No rows found for session_pitch
    except Exception as e:
        print(f"Error processing data for session_pitch {session_pitch}: {e}")
        return None

if __name__ == "__main__":
    load_data()
