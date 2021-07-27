import React from "react";
import Table from "react-bootstrap/Table";


const JobUtil = {
    convertJobRowsToTable: function(jobs) {
        if (jobs.length === 0) {
            return null;
        }
        const rows = [];
        for (let i = 0; i < jobs.length; i++) {
            const executedJob = jobs[i];
            rows.push(
                <tr>
                    <td>{executedJob['name']}</td>
                    <td>{executedJob['app_id']}</td>
                    <td>{executedJob['func']}</td>
                    <td>{executedJob['triggers']}</td>
                    <td>{executedJob['response']}</td>
                    <td>{executedJob['datetime_created']}</td>
                </tr>
            )
        }
        return (
            <Table striped bordered hover>
                <thead>
                <tr>
                    <th>Name</th>
                    <th>Id</th>
                    <th>Func</th>
                    <th>Triggers</th>
                    <th>Response</th>
                    <th>Datetime</th>
                </tr>
                </thead>
                <tbody>
                {rows}
                </tbody>
            </Table>
        )
    },
};


export default JobUtil;