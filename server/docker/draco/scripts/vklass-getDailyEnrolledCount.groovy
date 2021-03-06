// vklass-getDailyEnrolledCount
import org.apache.commons.io.IOUtils
import java.nio.charset.*

def flowFile = session.get();
if (flowFile == null) {
    return;
}

String nowISO8601 = (new Date()).format("yyyy-MM-dd'T'HH:mm:ss")
// String absenceId = "vklass_absence_" + (new Date()).format("yyyy-MM-dd")

def slurper = new groovy.json.JsonSlurper()

flowFile = session.write(flowFile,
    { inputStream, outputStream ->
        def text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        def obj = slurper.parseText(text)
        String absenceId = "vklass_absence_" + obj.schoolid.toString() + "_" + (new Date()).format("yyyy-MM-dd")
        String schoolId = "vklass_school_" + obj.schoolid.toString()
        int numEnrolled = obj.studentcount
        def builder = new groovy.json.JsonBuilder()
        builder.call {
            'id' absenceId
            'type' 'SchoolAttendanceObserved'
            'enrolled' {
                'type' 'Integer'
                'value' numEnrolled
            }
            'absent' {
                'type' 'studentAbsence'
                'value' []
            }
            'dateObserved' {
                'type' 'DateTime'
                'value' nowISO8601
            }
            'refSchool' {
                'type' 'Reference'
	    	    'value' schoolId
        	}
	        'source' {
		        'type' 'Text'
		        'value' 'http://www.vklass.se'
        	}
        }
        outputStream.write(builder.toPrettyString().getBytes(StandardCharsets.UTF_8))
    } as StreamCallback)
flowFile = session.putAttribute(flowFile, "filename", flowFile.getAttribute('filename').tokenize('.')[0]+'_translated.json')
session.transfer(flowFile, ExecuteScript.REL_SUCCESS)
