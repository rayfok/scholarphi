import React from "react";
import { DiscourseObj, RhetoricUnit } from "../../api/types";
import { Entities } from "../../state";
import { PDFPageView } from "../../types/pdfjs-viewer";
import * as uiUtils from "../../utils/ui";
import DiscourseTag from "../discourse/DiscourseTag";
import HighlightMask from "./HighlightMask";

interface Props {
  pageView: PDFPageView;
  entities: Entities;
  data: RhetoricUnit[];
  opacity: number;
  discourseToColorMap: { [discourse: string]: string };
}

/**
 * Declutter relevant sentences and add discourse tag in margin for each sentence.
 */
class DiscourseTagMask extends React.PureComponent<Props> {
  constructor(props: Props) {
    super(props);
  }

  render() {
    const { pageView, data, discourseToColorMap, opacity } = this.props;
    const pageNumber = uiUtils.getPageNumber(pageView);

    let discourseObjs = data
      .map((r: RhetoricUnit, index) => ({
        id: index.toString(),
        entity: r,
        label: r.label,
        bboxes: r.bboxes,
        tagLocation: r.bboxes[0],
        color: discourseToColorMap[r.label],
      }))
      .filter((e) => e.tagLocation.page === pageNumber);

    // If a sentence has multiple labels, define a prioritization so that each sentence has a unqiue label
    const text_to_labels: { [text: string]: DiscourseObj[] } = {};
    discourseObjs.forEach((x: DiscourseObj) => {
      if (!text_to_labels.hasOwnProperty(x.entity.text)) {
        text_to_labels[x.entity.text] = [];
      }
      text_to_labels[x.entity.text].push(x);
    });
    discourseObjs = Object.values(text_to_labels)
      .map((labels) => {
        const sortedLabels = labels.sort((firstEl, secondEl) => {
          if (firstEl.label === "Contribution") {
            return -1;
          } else if (firstEl.label === "Result") {
            return -1;
          } else {
            return 0;
          }
        });
        return sortedLabels;
      })
      .map((x: DiscourseObj[]) => x[0]);

    return (
      <>
        {discourseObjs.map((d) => (
          <DiscourseTag
            pageView={pageView}
            anchor={d.tagLocation}
            content={<span>{d.label}</span>}
            color={d.color}
            entityId={d.id}
            key={d.id}
          />
        ))}
        <HighlightMask
          pageView={pageView}
          discourseObjs={discourseObjs}
          opacity={opacity}
        />
      </>
    );
  }
}

export default DiscourseTagMask;
