import { useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

const ModalViewComment = (props) => {
  const { viewComment, show, setShow } = props;

  const handleClose = () => setShow(false);

  return (
    <>
      <Modal
        show={show}
        onHide={handleClose}
        size="lg"
        scrollable={true}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{`${viewComment?.username}'s comment`}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>ID: {viewComment?.id}</div>
          <div>Commnet: {viewComment?.comment}</div>
          <div>Like: {viewComment?.like}</div>
          <div>Sentiment: {viewComment?.sentiment}</div>
          <div>Time: {viewComment?.timeCreated}</div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default ModalViewComment;
