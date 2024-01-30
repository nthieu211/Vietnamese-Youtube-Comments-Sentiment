import "./HomePage.scss";
import ytSentLogo from "/yt-sent.svg";
import { useState } from "react";

const HomePage = () => {
  const [linkVideo, setLinkVideo] = useState("");

  return (
    <div className="home-container">
      <img src={ytSentLogo} className="logo" alt="logo" />
      <h2>Vietnamese Youtube Comments Sentiment</h2>
      <p>
        Paste your Youtube video link here, and we will analyze the sentiment of
        the comments.
      </p>
      <div className="input-container">
        <input
          type="text"
          placeholder="https://www.youtube.com/watch?v=..."
          value={linkVideo}
          onChange={(e) => setLinkVideo(e.target.value)}
        />
        <button>Submit</button>
      </div>
    </div>
  );
};

export default HomePage;
