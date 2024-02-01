import { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";
import { BarChart, Bar, XAxis, ResponsiveContainer, Tooltip } from "recharts";
import "./Result.scss";
import TableComments from "./TableComments";

const Result = (props) => {
  const result = {
    totalComments: 15,
    totalViews: 1000,
    totalLikes: 100,
    totalEnjoment: 1,
    totalDisgust: 2,
    totalSadness: 2,
    totalAnger: 3,
    totalSurprise: 4,
    totalFear: 1,
    totalOther: 2,

    comments: [
      {
        id: 1,
        username: "user1",
        comment: "comment1",
        sentiment: "positive",
        like: 10,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 2,
        username: "user2",
        comment: "comment2",
        sentiment: "negative",
        like: 20,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 3,
        username: "user3",
        comment: "comment3",
        sentiment: "neutral",
        like: 30,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 4,
        username: "user4",
        comment: "comment4",
        sentiment: "positive",
        like: 40,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 5,
        username: "user5",
        comment: "comment5",
        sentiment: "negative",
        like: 50,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 6,
        username: "user6",
        comment: "comment6",
        sentiment: "neutral",
        like: 60,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 7,
        username: "user7",
        comment: "comment7",
        sentiment: "positive",
        like: 70,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 8,
        username: "user8",
        comment: "comment8",
        sentiment: "negative",
        like: 80,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 9,
        username: "user9",
        comment: "comment9",
        sentiment: "neutral",
        like: 90,
        timeCreated: "2024-01-01 00:00:00",
      },
      {
        id: 10,
        username: "user10",
        comment: "comment10",
        sentiment: "positive",
        like: 100,
        timeCreated: "2024-01-01 00:00:00",
      },
    ],
  };
  const LIMIT_COMMENTS = 10;
  const [currentPage, setCurrentPage] = useState(0);
  const [pageCount, setPageCount] = useState(3);
  const [listComments, setListComments] = useState(result.comments);
  const [dataChart, setDataChart] = useState([
    {
      name: "Enjoyment",
      value: result.totalEnjoment,
      fill: "#8884d8",
    },
    {
      name: "Disgust",
      value: result.totalDisgust,
      fill: "#82ca9d",
    },
    {
      name: "Sadness",
      value: result.totalSadness,
      fill: "#ffc658",
    },
    {
      name: "Anger",
      value: result.totalAnger,
      fill: "#ffc658",
    },
    {
      name: "Surprise",
      value: result.totalSurprise,
      fill: "#ffc658",
    },
    {
      name: "Fear",
      value: result.totalFear,
      fill: "#ffc658",
    },
    {
      name: "Other",
      value: result.totalOther,
      fill: "#ffc658",
    },
  ]);

  const handlePageClick = (event) => {
    setCurrentPage(+event.selected + 1);
    //fetchnewdata
  };

  return (
    <div className="result-container container">
      <h2 className="title-result">Analyze Sentiment Result</h2>
      <div className="dashboard row">
        <div className="content-left col-lg-5 col-md-6 col-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Title video with link</h5>
            </div>
          </div>
          <div className="card">
            <div className="card-body d-flex flex-column text-center align-items-center">
              <h5 className="card-title">Total views</h5>
              <p className="card-text">{result.totalViews}</p>
            </div>
          </div>
          <div className="card">
            <div className="card-body d-flex flex-column text-center align-items-center">
              <h5 className="card-title">Total comments</h5>
              <p className="card-text">{result.totalComments}</p>
            </div>
          </div>
          <div className="card">
            <div className="card-body d-flex flex-column text-center align-items-center">
              <h5 className="card-title">Total video Like</h5>
              <p className="card-text">{result.totalLikes}</p>
            </div>
          </div>
        </div>
        <div className="content-right col-lg-7 col-md-6 col-12">
          <ResponsiveContainer width="90%" height="100%">
            <BarChart
              width={600}
              height={300}
              data={dataChart}
              margin={{
                top: 15,
                right: 20,
                left: 20,
                bottom: 15,
              }}
            >
              <XAxis dataKey="name" />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <TableComments currentComments={listComments} />
      <div className="paginate">
        <ReactPaginate
          nextLabel="next >"
          onPageChange={handlePageClick}
          pageRangeDisplayed={5}
          pageCount={pageCount}
          previousLabel="< previous"
          pageClassName="page-item"
          pageLinkClassName="page-link"
          previousClassName="page-item"
          previousLinkClassName="page-link"
          nextClassName="page-item"
          nextLinkClassName="page-link"
          breakLabel="..."
          breakClassName="page-item"
          breakLinkClassName="page-link"
          containerClassName="pagination"
          activeClassName="active"
          renderOnZeroPageCount={null}
          forcePage={0}
        />
      </div>
    </div>
  );
};

export default Result;
