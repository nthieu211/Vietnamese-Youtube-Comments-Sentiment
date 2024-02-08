import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import { useTranslation } from "react-i18next";

const ModalViewComment = (props) => {
  const { viewComment, show, setShow } = props;
  const { t, i18n } = useTranslation();
  const handleClose = () => setShow(false);

  function formatDateTime(datetimeString) {
    const date = new Date(datetimeString);
    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      hour12: false,
    };
    if (i18n.language === "vi") {
      return date.toLocaleString("vi-VN", options);
    } else {
      return date.toLocaleString("en-US", options);
    }
  }

  return (
    <>
      <Modal
        show={show}
        onHide={handleClose}
        size="md"
        scrollable={true}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{t("result.detailComment")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h5>ID</h5>
          <span>{viewComment?.id}</span>
          <hr />
          <h5>{t("result.username")}</h5>
          <span>{viewComment?.username}</span>
          <hr />
          <h5>{t("result.comment")}</h5>
          <span>{viewComment?.comment}</span>
          <hr />
          <h5>{t("result.like")}</h5>
          <span>{viewComment?.like}</span>
          <hr />
          <h5>{t("result.sentiment")}</h5>
          <span>{props.getSentiment(viewComment?.sentiment)}</span>
          <hr />
          <h5>{t("result.time")}</h5>
          <span>{formatDateTime(viewComment?.timeCommented)}</span>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleClose}>
            {t("result.close")}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default ModalViewComment;
