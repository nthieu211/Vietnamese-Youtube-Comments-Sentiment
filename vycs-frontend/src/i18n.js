import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

i18n
  // detect user language
  // learn more: https://github.com/i18next/i18next-browser-languageDetector
  .use(LanguageDetector)
  // pass the i18n instance to react-i18next.
  .use(initReactI18next)
  // init i18next
  // for all options read: https://www.i18next.com/overview/configuration-options
  .init({
    debug: true,
    fallbackLng: "en",
    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    },
    resources: {
      en: {
        translation: {
          homepage: {
            title: "Vietnamese Youtube Comments Sentiment",
            describe:
              "Paste your Youtube video link here, and we will analyze the sentiment of the comments.",
            textPlaceholder: "Paste your Youtube video link here",
            button: "Analyze",
            errorOccurred: "An error occurred!",
            invalidYoutubeLink: "Invalid Youtube video link!",
          },
          header: {
            home: "Home",
            model: "About Model",
          },
          result: {
            totalViews: "Total views",
            totalLikes: "Total likes",
            totalComments: "Total comments",
            analyzedComments: "Analyzed comments",
            username: "Username",
            comment: "Comment",
            like: "Like",
            sentiment: "Sentiment",
            enjoyment: "Enjoyment",
            disgust: "Disgust",
            sadness: "Sadness",
            anger: "Anger",
            surprise: "Surprise",
            fear: "Fear",
            other: "Other",
            detailComment: "Detail Comment",
            time: "Time",
            previous: "Previous",
            next: "Next",
            close: "Close",
          },
          aboutModel: {
            title: {
              dataset: "Dataset",
              model: "Model",
              modelResult: "Model Result",
              ref: "References",
            },
            vsmec:
              "The dataset contains 6,927 emotion-annotated sentences with 7 emotions (enjoyment, disgust, sadness, anger, surprise, fear and others). The authors of the article tried to apply machine learning and deep neural network models with UIT-VSMEC. Among the tested models, the Convolutional Neural Network (CNN) model performed the best, achieving a weighted F1-score of 59.74%.",
            splitdata: {
              title: "From 6,927 sentences divided into 3 subset:",
              train: "Training set:",
              valid: "Validation set:",
              test: "Test set:",
              sentences: "sentences",
            },
            model: {
              phobert1:
                "The first public large-scale monolingual language models pre-trained for Vietnamese. Models using a 20GB word-level Vietnamese corpus with (~1GB ) Vietnamese Wikipedia and (~19GB) generated from Vietnamese news corpus.",
              phobert2:
                "Base on pre-trained PhoBERT-base, the model using PhoBERT to extract features then classify 7 emotion labels of the data set.",
              result:
                "The model achieved a weighted F1-score of <b>64%</b> on the test set.",
            },
          },
        },
      },
      vi: {
        translation: {
          homepage: {
            title: "Phân tích cảm xúc bình luận tiếng Việt trên Youtube",
            describe:
              "Dán đường dẫn video Youtube của bạn ở đây, và chúng tôi sẽ phân tích cảm xúc của các bình luận tiếng Việt.",
            textPlaceholder: "Dán đường dẫn video Youtube của bạn ở đây",
            button: "Phân tích",
            errorOccurred: "Đã xảy ra lỗi!",
            invalidYoutubeLink: "Đường dẫn video Youtube không hợp lệ!",
          },
          header: {
            home: "Trang chủ",
            model: "Về mô hình",
          },
          result: {
            totalViews: "Tổng lượt xem",
            totalLikes: "Tổng lượt thích",
            totalComments: "Tổng bình luận",
            analyzedComments: "Bình luận đã phân tích",
            username: "Tên người dùng",
            comment: "Bình luận",
            like: "Lượt thích",
            sentiment: "Cảm xúc",
            enjoyment: "Vui vẻ",
            disgust: "Ghê tởm",
            sadness: "Buồn bã",
            anger: "Tức giận",
            surprise: "Ngạc nhiên",
            fear: "Sợ hãi",
            other: "Khác",
            detailComment: "Chi tiết bình luận",
            time: "Thời gian bình luận",
            previous: "Trước",
            next: "Sau",
            close: "Đóng",
          },
          aboutModel: {
            title: {
              dataset: "Bộ dữ liệu",
              model: "Mô hình",
              modelResult: "Kết quả mô hình",
              ref: "Tài liệu tham khảo",
            },
            vsmec:
              "Bộ dữ liệu chứa 6,927 câu được gán nhãn cảm xúc với 7 cảm xúc (vui vẻ, ghê tởm, buồn bã, tức giận, ngạc nhiên, sợ hãi và khác). Tác giả của bài báo đã thử áp dụng các mô hình học máy và mạng nơ-ron sâu với UIT-VSMEC. Trong số các mô hình được thử nghiệm, mô hình Convolutional Neural Network (CNN) đã đạt kết quả tốt nhất với F1-score 59.74%.",
            splitdata: {
              title: "Từ 6,927 câu chia thành 3 tập con:",
              train: "Tập huấn luyện:",
              valid: "Tập kiểm tra:",
              test: "Tập thử nghiệm:",
              sentences: "câu",
            },
            model: {
              phobert1:
                "Mô hình pre-trained đơn ngôn ngữ quy mô lớn đầu tiên cho tiếng Việt. Mô hình sử dụng bộ dữ liệu tiếng Việt cấp từ vựng 20GB với (~1GB) Wikipedia tiếng Việt và (~19GB) được tạo từ bộ dữ liệu tin tức tiếng Việt.",
              phobert2:
                "Dựa trên PhoBERT-base đã được huấn luyện trước, mô hình sử dụng PhoBERT để trích xuất đặc trưng sau đó phân loại 7 nhãn cảm xúc của tập dữ liệu.",
              result: "Mô hình đạt F1-score 64% trên tập thử nghiệm.",
            },
          },
        },
      },
    },
  });

export default i18n;
