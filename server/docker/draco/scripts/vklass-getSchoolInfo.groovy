// vklass-getSchoolInfo
import org.apache.commons.io.IOUtils
import java.nio.charset.*

def flowFile = session.get();
if (flowFile == null) {
    return;
}

def slurper = new groovy.json.JsonSlurper()

flowFile = session.write(flowFile,
    { inputStream, outputStream ->
        def text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        def obj = slurper.parseText(text)
        String schoolId = "vklass_school_" + obj.schoolid.toString()
        String schoolName = obj.schoolname
        int numStudents = obj.studentcount
        int numStaff = obj.personalcount
        // log.warn("****************************** " + numStaff.toString())
        def builder = new groovy.json.JsonBuilder()
        builder.call {
            'id' schoolId
            'type' 'School'
            'source' {
                'value' 'http://www.vklass.se'
            }
            'name' {
                'type' 'Text'
                'value' schoolName
            }
            'logo' {
                'type' 'URL'
                'value' 'https://vignette.wikia.nocookie.net/harrypotter/images/a/ae/Hogwartscrest.png'
            }
            'identifier' {
                'type' 'Text'
	    	    'value' '112233-4455'
        	}
            'studentCount' {
                'type' 'Integer'
	    	    'value' numStudents
        	}
	        'staffCount' {
		        'type' 'Integer'
		        'value' numStaff
        	}
        }
        outputStream.write(builder.toPrettyString().getBytes(StandardCharsets.UTF_8))
    } as StreamCallback)
flowFile = session.putAttribute(flowFile, "filename", flowFile.getAttribute('filename').tokenize('.')[0]+'_translated.json')
session.transfer(flowFile, ExecuteScript.REL_SUCCESS)
