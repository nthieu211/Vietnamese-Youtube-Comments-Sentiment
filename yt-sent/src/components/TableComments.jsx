import { useState } from "react";
import ModalViewComment from "./ModalViewComment";

const TableComments = (props) => {
  const { currentComments } = props;
  const [viewComment, setViewComment] = useState({});
  const [show, setShow] = useState(false);
  const handleView = (cmt) => {
    setViewComment(cmt);
    setShow(true);
  };

  return (
    <>
      <table className="table table-hover table-comments table-responsive-sm">
        <thead>
          <tr className="table-danger">
            <th scope="col">Username</th>
            <th scope="col">Comment</th>
            <th scope="col">Like</th>
            <th scope="col">Sentiment</th>
          </tr>
        </thead>
        <tbody>
          {currentComments &&
            currentComments.length > 0 &&
            currentComments.map((cmt, index) => {
              return (
                <tr key={`cmt-${index}`} onClick={() => handleView(cmt)}>
                  <td>{cmt.username}</td>
                  <td>{cmt.comment}</td>
                  <td>{cmt.like}</td>
                  <td>{cmt.sentiment}</td>
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
      />
    </>
  );
};

export default TableComments;
