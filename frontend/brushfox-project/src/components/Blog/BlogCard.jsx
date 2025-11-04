import { Link } from 'react-router-dom';
import { formatDate, truncateText } from '../../utils/helpers';
import './BlogCard.css';

const BlogCard = ({ post }) => {
  return (
    <article className="blog-card">
      <div className="blog-card-header">
        <h2 className="blog-card-title">
          <Link to={`/blog/${post.slug}`}>{post.title}</Link>
        </h2>
        <div className="blog-card-meta">
          <span className="author">👤 {post.author?.username || 'Autor'}</span>
          <span className="date">📅 {formatDate(post.created)}</span>
        </div>
      </div>
      
      <div className="blog-card-content">
        <p>{truncateText(post.post, 200)}</p>
      </div>
      
      <div className="blog-card-footer">
        <Link to={`/blog/${post.slug}`} className="read-more">
          Czytaj więcej →
        </Link>
      </div>
    </article>
  );
};

export default BlogCard;
