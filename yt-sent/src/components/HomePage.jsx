import "./HomePage.scss";
import ytSentLogo from "/yt-sent.svg";
import { ImSpinner2 } from "react-icons/im";
import { useState } from "react";
import { toast } from "react-toastify";

const HomePage = () => {
  const [linkVideo, setLinkVideo] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const validateLink = (url) => {
    var p =
      /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
    var matches = url.match(p);
    if (matches) {
      return matches[1];
    }
    return false;
  };

  const submitLink = async () => {
    const videoId = validateLink(linkVideo);
    if (videoId) {
      await callApi();
      setIsLoading(false);
      toast.success(`Video ID: ${videoId}`);
    } else {
      setIsLoading(false);
      toast("Invalid Youtube video link!");
    }
  };

  const callApi = () => {
    // fake api call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve();
      }, 2000);
    });
  };

  return (
    <div className="home-container container text-center">
      <img src={ytSentLogo} className="logo" alt="logo" />
      <div className="title">
        <h1>Vietnamese Youtube Comments Sentiment</h1>
        <p>
          Paste your Youtube video link here, and we will analyze the sentiment
          of the comments.
        </p>
      </div>
      <div className="col-lg-6 col-md-8 col-11 mx-auto mt-5">
        <div className="input-group">
          <input
            type="url"
            className="form-control video-link"
            value={linkVideo}
            placeholder="Paste Youtube video link here"
            aria-label="Youtube Video"
            onChange={(e) => setLinkVideo(e.target.value)}
          />
          <button
            type="button"
            className="btn btn-danger btn-analyze"
            disabled={isLoading}
            onClick={() => {
              setIsLoading(true);
              submitLink();
            }}
          >
            {isLoading && <ImSpinner2 className="loading-icon" />}
            Analyze
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
