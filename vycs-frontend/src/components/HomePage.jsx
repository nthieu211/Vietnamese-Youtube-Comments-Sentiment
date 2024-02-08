import "./HomePage.scss";
import ytSentLogo from "/images/yt-sent.svg";
import { ImSpinner2 } from "react-icons/im";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useTranslation } from "react-i18next";
import { postAnalyze } from "../services/apiServices";

const HomePage = () => {
  const [linkVideo, setLinkVideo] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { t } = useTranslation();

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
      let res = await postAnalyze(videoId);
      if (res && res.data.EC === 0) {
        setIsLoading(false);
        navigate(`/result/${videoId}`);
      } else {
        setIsLoading(false);
        toast(res?.data?.EM || t("homepage.errorOccurred"));
      }
    } else {
      setIsLoading(false);
      toast(t("homepage.invalidYoutubeLink"));
    }
    setIsLoading(false);
  };

  return (
    <div className="home-container container text-center">
      <img src={ytSentLogo} className="logo" alt="logo" />
      <div className="title">
        <h1>{t("homepage.title")}</h1>
        <p>{t("homepage.describe")}</p>
      </div>
      <div className="col-lg-6 col-md-8 col-11 mx-auto mt-5">
        <div className="input-group">
          <input
            type="url"
            className="form-control video-link"
            value={linkVideo}
            placeholder={t("homepage.textPlaceholder")}
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
            {t("homepage.button")}
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
