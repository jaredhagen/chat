import { Comment } from "antd";

export default function Message({ author, content }) {
  return <Comment author={author} content={content}></Comment>;
}
