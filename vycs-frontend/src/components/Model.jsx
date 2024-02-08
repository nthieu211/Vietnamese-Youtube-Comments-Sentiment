import "./Model.scss";
import { useTranslation } from "react-i18next";

const Model = () => {
  const { t } = useTranslation();
  return (
    <div className="about-model-container container col-10">
      <h1 className="title">{t("aboutModel.title.dataset")}</h1>
      <h3 className="mt-4">
        <a
          href="https://arxiv.org/abs/1911.09339"
          target="_blank"
          className="text-decoration-none"
        >
          UIT-VSMEC (2019)
        </a>{" "}
        - Emotion Recognition for Vietnamese Social Media Text
      </h3>
      <div className="model-content">
        <p>{t("aboutModel.vsmec")} </p>
        <p>{t("aboutModel.splitdata.title")} </p>
        <ul>
          <li>
            <b>{t("aboutModel.splitdata.train")}</b> 5548{" "}
            {t("aboutModel.splitdata.sentences")}{" "}
          </li>
          <li>
            <b>{t("aboutModel.splitdata.valid")}</b> 686{" "}
            {t("aboutModel.splitdata.sentences")}{" "}
          </li>
          <li>
            <b>{t("aboutModel.splitdata.test")}</b> 693{" "}
            {t("aboutModel.splitdata.sentences")}{" "}
          </li>
        </ul>
      </div>
      <h1 className="title">{t("aboutModel.title.model")}</h1>
      <h3 className="mt-4">
        <a
          href="https://arxiv.org/abs/2003.00744"
          target="_blank"
          className="text-decoration-none"
        >
          PhoBERT (2020)
        </a>{" "}
        - Pre-trained language models for Vietnamese
      </h3>
      <div className="model-content">
        <p>
          {t("aboutModel.model.phobert1")} <br />
        </p>
        <p>
          {t("aboutModel.model.phobert2")} <br />
        </p>
      </div>
      <h3 className="mt-5">{t("aboutModel.title.modelResult")}</h3>
      <div className="model-content">
        <p>
          {t("aboutModel.model.result")} <br />
        </p>
        <table class="table table-bordered table-fixed">
          <thead>
            <tr>
              <th className="w-25" scope="col">
                #
              </th>
              <th className="w-25" scope="col">
                First
              </th>
              <th className="w-25" scope="col">
                Second
              </th>
              <th className="w-25" scope="col">
                Third
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Learning rate</th>
              <td>1.0e-5</td>
              <td>1.0e-5</td>
              <td>1.0e-5</td>
            </tr>
            <tr>
              <th scope="row">Weight decay</th>
              <td>1.0e-3</td>
              <td>1.0e-2</td>
              <td>1.0e-2</td>
            </tr>
            <tr>
              <th scope="row">LR scheduler</th>
              <td>OneCycleLR</td>
              <td>ReduceLROnPlateau</td>
              <td>ReduceLROnPlateau</td>
            </tr>
            <tr>
              <th scope="row">Linear layer</th>
              <td>None</td>
              <td>512</td>
              <td>256</td>
            </tr>
            <tr>
              <th scope="row">Drop-out</th>
              <td>0.3</td>
              <td>0.4</td>
              <td>0.5</td>
            </tr>
            <tr>
              <th scope="row">Batch size</th>
              <td>16</td>
              <td>16</td>
              <td>8</td>
            </tr>
            <tr>
              <th scope="row">Valid F1-score</th>
              <td>0.5985</td>
              <td>0.6179</td>
              <td>
                <b>0.6268</b>
              </td>
            </tr>
            <tr>
              <th scope="row">Valid Accuracy</th>
              <td>0.6137</td>
              <td>0.6224</td>
              <td>
                <b>0.6283</b>
              </td>
            </tr>
            <tr>
              <th scope="row">Test F1-score</th>
              <td>0.5892</td>
              <td>0.6291</td>
              <td>
                <b>0.6396</b>
              </td>
            </tr>
            <tr>
              <th scope="row">Test Accuracy</th>
              <td>0.5931</td>
              <td>0.6291</td>
              <td>
                <b>0.6407</b>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h3 className="mt-5">{t("aboutModel.title.ref")}</h3>
      <div className="model-content">
        <ul>
          <li>
            <a
              href="https://arxiv.org/abs/1911.09339"
              target="_blank"
              className="text-decoration-none"
            >
              1. Emotion Recognition for Vietnamese Social Media Text
            </a>
          </li>
          <li>
            <a
              href="https://arxiv.org/abs/2003.00744"
              target="_blank"
              className="text-decoration-none"
            >
              2. PhoBERT: Pre-trained language models for Vietnamese
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Model;
