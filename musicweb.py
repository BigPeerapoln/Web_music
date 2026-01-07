import streamlit as st

# --- Song Class ---
class Song:
    def __init__(self, title, artist, audio_data=None):
        self.title = title
        self.artist = artist
        self.audio_data = audio_data  # เก็บข้อมูลไฟล์เพลง
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_data):
        new_song = Song(title, artist, audio_data)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        if self.head is None:
            return []
        playlist_songs = []
        current = self.head
        count = 1
        while current:
            status = "▶️" if current == self.current_song else ""
            playlist_songs.append(f"{count}. {status} {current.title} - {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist.")

    def prev_song(self):
        if self.head is None or self.current_song == self.head:
            st.warning("Beginning of playlist.")
            return
        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def delete_song(self, title):
        if self.head is None: return
        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            return

        current = self.head
        while current.next_song and current.next_song.title != title:
            current = current.next_song

        if current.next_song:
            if self.current_song == current.next_song:
                self.current_song = current.next_song.next_song or current
            current.next_song = current.next_song.next_song
            self.length -= 1

# --- Streamlit App Layout ---
st.set_page_config(page_title="Music Player", layout="wide")
st.title("🎶 Modern Music Playlist")

if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# --- Sidebar: Upload & Add ---
with st.sidebar:
    st.header("💿 Add New Track")
    new_title = st.text_input("Song Title")
    new_artist = st.text_input("Artist")
    uploaded_file = st.file_uploader("Browse Audio File", type=['mp3', 'wav', 'ogg'])

    if st.button("➕ Add to Playlist"):
        if new_title and new_artist and uploaded_file:
            st.session_state.playlist.add_song(new_title, new_artist, uploaded_file)
        else:
            st.error("Please fill all fields and upload a file.")

    st.divider()
    st.header("🗑️ Remove Track")
    del_title = st.text_input("Title to Delete")
    if st.button("Delete"):
        st.session_state.playlist.delete_song(del_title)

# --- Main Interface ---
col_list, col_player = st.columns([1, 1])

with col_list:
    st.header("📜 Playlist")
    songs = st.session_state.playlist.display_playlist()
    if songs:
        for s in songs:
            st.write(s)
    else:
        st.info("No songs added yet.")

with col_player:
    st.header("🎵 Now Playing")
    curr = st.session_state.playlist.current_song
    if curr:
        st.subheader(f"{curr.title}")
        st.text(f"Artist: {curr.artist}")

        # ส่วนสำคัญ: เล่นไฟล์เสียงที่ Browse เข้ามา
        if curr.audio_data:
            st.audio(curr.audio_data)

        # Controls
        c1, c2, c3 = st.columns(3)
        if c1.button("⏪ Prev"):
            st.session_state.playlist.prev_song()
            st.rerun()
        if c2.button("🔄 Refresh"):
            st.rerun()
        if c3.button("⏩ Next"):
            st.session_state.playlist.next_song()
            st.rerun()
    else:
        st.write("Select a song to play.")

st.divider()
st.caption(f"Total tracks: {st.session_state.playlist.length}")
