import { useState } from "react";
import { useTranslation } from "react-i18next";
import ModalViewComment from "./ModalViewComment";

const TableComments = (props) => {
  const { t } = useTranslation();
  const { currentComments } = props;
  const [viewComment, setViewComment] = useState({});
  const [show, setShow] = useState(false);
  const handleView = (cmt) => {
    setViewComment(cmt);
    setShow(true);
  };

  const getSentiment = (sentiment) => {
    switch (sentiment) {
      case "Enjoyment":
        return t("result.enjoyment");
      case "Disgust":
        return t("result.disgust");
      case "Sadness":
        return t("result.sadness");
      case "Anger":
        return t("result.anger");
      case "Surprise":
        return t("result.surprise");
      case "Fear":
        return t("result.fear");
      default:
        return t("result.other");
    }
  };

  return (
    <>
      <table className="table table-hover table-comments table-responsive-sm">
        <thead>
          <tr className="table-danger">
            <th scope="col">
              <span className="d-none d-sm-table-cell">
                {t("result.username")}
              </span>
            </th>
            <th scope="col">{t("result.comment")}</th>
            <th scope="col">{t("result.like")}</th>
            <th scope="col">{t("result.sentiment")}</th>
          </tr>
        </thead>
        <tbody>
          {currentComments &&
            currentComments.length > 0 &&
            currentComments.map((cmt, index) => {
              return (
                <tr key={`cmt-${index}`} onClick={() => handleView(cmt)}>
                  <td>
                    <span className="d-none d-sm-table-cell">
                      {cmt?.username?.length > 13
                        ? `${cmt?.username?.substring(0, 13)}...`
                        : cmt?.username}
                    </span>
                  </td>
                  <td>
                    {cmt?.comment?.length > 115
                      ? `${cmt?.comment?.substring(0, 115)}...`
                      : cmt?.comment}
                  </td>
                  <td>{cmt?.like}</td>
                  <td>{getSentiment(cmt?.sentiment)}</td>
                </tr>
              );
            })}
          {currentComments && currentComments.length === 0 && (
            <tr>
              <td colSpan="4">Not found data</td>
            </tr>
          )}
        </tbody>
      </table>
      <ModalViewComment
        show={show}
        setShow={setShow}
        viewComment={viewComment}
        getSentiment={getSentiment}
      />
    </>
  );
};

export default TableComments;
