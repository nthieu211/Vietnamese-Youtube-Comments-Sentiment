import { useEffect, useState } from "react";
import ReactPaginate from "react-paginate";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, ResponsiveContainer, Tooltip } from "recharts";
import "./Result.scss";
import TableComments from "./TableComments";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { getResult } from "../services/apiServices";

const Result = (props) => {
  const { videoId } = useParams();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState(1);
  const [pageCount, setPageCount] = useState(1);
  const [listComments, setListComments] = useState([]);
  const [dataChart, setDataChart] = useState([]);
  const [dataDashboard, setDataDashboard] = useState({});

  let formatter = Intl.NumberFormat("en", { notation: "compact" });

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{`${label} : ${payload[0].value}`}</p>
        </div>
      );
    }

    return null;
  };

  const convert2DataChart = (data) => {
    setDataChart([
      {
        name: t("result.enjoyment"),
        value: data.totalEnjoment,
        fill: "#82ca9d",
      },
      {
        name: t("result.disgust"),
        value: data.totalDisgust,
        fill: "#8884d8",
      },
      {
        name: t("result.sadness"),
        value: data.totalSadness,
        fill: "#8dbce3",
      },
      {
        name: t("result.anger"),
        value: data.totalAnger,
        fill: "#f04135",
      },
      {
        name: t("result.surprise"),
        value: data.totalSurprise,
        fill: "#ffc658",
      },
      {
        name: t("result.fear"),
        value: data.totalFear,
        fill: "#fc9d5b",
      },
      {
        name: t("result.other"),
        value: data.totalOther,
        fill: "#a8d1d1",
      },
    ]);
  };

  useEffect(() => {
    fetchResult(videoId, currentPage);
  }, [currentPage]);

  const fetchResult = async (videoId, currentPage, sortBy = "like") => {
    let res = await getResult(videoId, currentPage, sortBy);
    console.log(res);
    if (res && res.data.EC === 0) {
      if (res?.data?.data?.comments?.length === 0) {
        toast("Not found data");
      }
      setPageCount(res?.data?.data?.totalPages);
      setListComments(res?.data?.data?.comments);
      convert2DataChart(res?.data?.data);
      setDataDashboard({
        title: res?.data?.data?.title,
        totalViews: res?.data?.data?.totalViews,
        totalLikes: res?.data?.data?.totalLikes,
        totalComments: res?.data?.data?.totalComments,
        totalCommentAnalyzed: res?.data?.data?.totalCommentAnalyzed,
      });
    } else {
      navigate("/not-found");
    }
  };

  const handlePageClick = (event) => {
    setCurrentPage(+event.selected + 1);
  };

  return (
    <div className="result-container container">
      <h3 className="title-result">
        <a href={`https://www.youtube.com/watch?v=${videoId}`} target="_blank">
          {dataDashboard?.title?.length > 60
            ? `${dataDashboard?.title?.substring(0, 60)}...`
            : dataDashboard?.title}
        </a>
      </h3>
      <div className="dashboard row">
        <div className="content-left col-lg-5 col-md-6 col-12">
          <div className="card">
            <div className="card-body flex-column text-center align-items-center">
              <div className="card-title">{t("result.totalViews")}</div>
              <div className="card-text">
                {formatter.format(dataDashboard?.totalViews)}
              </div>
            </div>
          </div>
          <div className="card">
            <div className="card-body flex-column text-center align-items-center">
              <div className="card-title">{t("result.totalLikes")}</div>
              <div className="card-text">
                {formatter.format(dataDashboard?.totalLikes)}
              </div>
            </div>
          </div>
          <div className="card">
            <div className="card-body flex-column text-center align-items-center">
              <div className="card-title">{t("result.totalComments")}</div>
              <div className="card-text">{dataDashboard?.totalComments}</div>
            </div>
          </div>
          <div className="card">
            <div className="card-body flex-column text-center align-items-center">
              <div className="card-title">{t("result.analyzedComments")}</div>
              <div className="card-text">
                {dataDashboard?.totalCommentAnalyzed}
              </div>
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
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <TableComments currentComments={listComments} />
      <div className="paginate">
        <ReactPaginate
          nextLabel={`${t("result.next")} >`}
          onPageChange={handlePageClick}
          pageRangeDisplayed={3}
          pageCount={pageCount}
          previousLabel={`< ${t("result.previous")}`}
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
