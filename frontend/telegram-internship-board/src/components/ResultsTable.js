import React from 'react';

const ResultsTable = ({ data }) => {
  if (data.length === 0) {
    return <div className="no-data">No data available</div>;
  }

  return (
    <div className="table-container">
      <div className="table-wrapper">
        <table className="results-table">
          <thead>
            <tr>
              <th>Type</th>
              <th className="company-col">Company</th>
              <th className="wrap">Position</th>
              <th className="wrap">Qualif.</th>
              <th>Batch</th>
              <th className="exp-wrap">Experience</th>
              <th className="wrap">Location</th>
              <th>Mode</th>
              <th>Stipend</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {data.map((job, index) => (
              <tr key={index}>
                <td>{job.type}</td>
                <td className="company-col">{job.company}</td>
                <td className="wrap">{job.position}</td>
                <td className="wrap">{job.qualification}</td>
                <td>{job.batch}</td>
                <td className="exp-wrap">{job.experience}</td>
                <td className="wrap">{job.location}</td>
                <td>{job.mode}</td>
                <td>{job.stipend}</td>
                <td>
                  <a href={job.apply_link} target="_blank" rel="noopener noreferrer">
                    Apply
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Styling */}
      <style>{`
        .table-container {
          padding: 16px;
        }

        .table-wrapper {
          overflow-x: auto;
          max-width: 100%;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
        }

        .results-table {
          width: 100%;
          min-width: 720px;
          border-collapse: collapse;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          font-size: 14px;
        }

        .results-table th, .results-table td {
          padding: 8px 10px;
          border: 1px solid #e5e7eb;
          text-align: left;
          vertical-align: top;
        }

        .results-table thead {
          background-color: #1f2937;
          color: white;
        }

        .results-table tr:nth-child(even) {
          background-color: #f9fafb;
        }

        .results-table tr:hover {
          background-color: #f3f4f6;
        }

        .results-table a {
          color: #2563eb;
          text-decoration: none;
          font-weight: 500;
        }

        .results-table a:hover {
          text-decoration: underline;
        }

        .wrap {
          white-space: normal;
          word-break: break-word;
          max-width: 160px;
        }

        .company-col {
          max-width: 100px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .exp-wrap {
          max-width: 140px;
          white-space: normal;
          word-break: break-word;
        }

        .no-data {
          padding: 20px;
          text-align: center;
          font-size: 18px;
          color: #6b7280;
        }
      `}</style>
    </div>
  );
};

export default ResultsTable;
